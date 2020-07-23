
                    #include <sys/types.h>
                    #include <sys/socket.h>
                    #include <sys/ioctl.h>
                    #include <net/if.h>
                    #include <netinet/in.h>
                    #include <netinet/in_var.h>
                    #include <arpa/inet.h>
                    
                    int main(void) {
                        int fd = socket (AF_INET6, SOCK_DGRAM, IPPROTO_IPV6);
                        struct in6_ifreq ifreq;

                        ioctl(fd, SIOCGIFAFLAG_IN6, &ifreq);

                        return 0;
                    }
                    