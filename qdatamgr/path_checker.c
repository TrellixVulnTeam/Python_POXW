/**
 * gcc -g -o path_checker path_checker.c -laio  # build exe
 * gcc -g -fPIC -shared -o path_checker.so  path_checker.c -laio # build dll
 */
#define _GNU_SOURCE           /* O_DIRECT is not POSIX */
#include <stdio.h>            /* for perror() */
#include <unistd.h>           /* for syscall() */
#include <fcntl.h>            /* O_RDWR */
#include <string.h>           /* memset() */
#include <inttypes.h>         /* uint64_t */
#include <linux/fs.h>         /* BLKBSZGET */
#include <errno.h>            /* errno */
#include <stdlib.h>

#include <libaio.h>

//#define BUF_SIZE (4096)


int path_checker(const char *path, int timeout_sec)
{
    io_context_t ctx;
    struct iocb cb;
    struct iocb *cbs[1];
    unsigned char *buf;
    struct io_event events[1];
    struct timespec timeout = { .tv_sec = 1, .tv_nsec = 0 };
    int ret;
    int fd;
    int blksize=512;
    unsigned long pgsize = getpagesize();

    timeout.tv_sec = timeout_sec;

    fd = open(path, O_RDONLY | O_DIRECT);
    if (fd < 0) {
        perror("open device error");
        goto err;
    }

    if (ioctl(fd, BLKBSZGET, &blksize) < 0) {
        // cannot get blocksize, set default
        fprintf(stderr, "BLKBSZGET failed: %s", strerror(errno));
        blksize = 512;
    }
    if (blksize > 4096) {
        /*
         *          * Sanity check for DASD; BSZGET is broken
         *                   */
        blksize = 4096;
    }

    ret = posix_memalign((void **)&buf, blksize, (blksize + 1));
    if (ret < 0) {
        perror("posix_memalign failed");
        goto err1;
    }
    memset(buf, 0, blksize + 1);

    ctx = 0;
    ret = io_setup(1, &ctx);
    if (ret < 0) {
        fprintf(stderr, "io_setup error:%s \n", strerror(-ret));
        goto err2;
    }


    /* setup I/O control block */
    io_prep_pread(&cb, fd, buf, blksize, 0);

    //cb.data = main;

    cbs[0] = &cb;
    ret = io_submit(ctx, 1, cbs);
    if (ret != 1) {
        if (ret < 0) {
            fprintf(stderr, "io_submit error:%s \n", strerror(-ret));
        } else {
            fprintf(stderr, "could not sumbit IOs \n ");
        }
        goto err3;
    }

    /* get the reply */
    errno = 0;
    ret = io_getevents(ctx, 1, 1, events, &timeout);

    // On  success,  io_getevents()  returns the number of events read: 0 if no events are available, or less than min_nr if the timeout has elapsed.  min_nr=1 now.
    if (ret != 1) {
        if (ret < 0) {
            fprintf(stderr, "io_getevents error:%s \n", strerror(-ret));
        } else {
            fprintf(stderr, "could not get Events.\n");
        }
        ret = io_cancel(ctx, cbs[0], events);
        if (ret) {
            fprintf(stderr, "could not cancel io. \n");
        }
        goto err3;
    }
    if (events[0].res == blksize) {
        printf("path: %s is health. \n", path);
    } else {
        fprintf(stderr, "path: %s is error. error message: %s \n", path, strerror(-events[0].res));
        goto err3;
    }

    //printf("%s\n", buf);

    if ((ret = io_destroy(ctx)) < 0) {
        fprintf(stderr, "io_destroy error:%s \n ", strerror(-ret));
        goto err2;
    }

    free(buf);
    close(fd);
    return 0;

    err3:
    if ((ret = io_destroy(ctx)) < 0)
        fprintf(stderr, "io_destroy error:%s \n ", strerror(-ret));
    err2:
    free(buf);
    err1:
    close(fd);
    err:
    return -1;
}

int main(int argc, char **argv)
{

    char version[8]="v2.3";

    // check usage
    if ((argc > 3) || (argc < 2) ){
        fprintf(stderr, "need 2 args, have %d args\n", argc - 1);
        fprintf(stderr, "%s Version %s \n", argv[0], version);
        fprintf(stderr, "Usage: %s <device path> [timeout]\n", argv[0]);
        fprintf(stderr, "for example: %s /dev/sdb 1\n", argv[0]);
        exit(-1);
    }

    return path_checker(argv[1], atoi(argv[2]));
}
