
#include <stdio.h>
#include <unistd.h>
#include <pthread.h>
#include <unistd.h>			//Needed for I2C port
#include <fcntl.h>			//Needed for I2C port
#include <sys/ioctl.h>			//Needed for I2C port
#include <linux/i2c-dev.h>		//Needed for I2C port

typedef  unsigned char uint8_t;


void* Motorcontrol (void* param);  //thread function
void  Motorinit();



uint8_t MotorHF[7] = {7,3,0xa5,2,3,0xa5,2}; 
// High speed forward left + right; add explanation

uint8_t MotorST[7] = {7,0,0,0,0,0,0};
// Stop left + right; add explanation

uint8_t MotorHR[7] = {7,3,0xa5,1,3,0xa5,1};
//High speed reverse left + right; add explanation

int fd;
char *filename = (char*)"/dev/i2c-1";

void Motorinit()
{
    uint8_t Totalpower[2]={4,250};     // power between 0 and 255
    uint8_t Softstart[3]={0x91,23,0};  // add explanation


    
    //pullUpDnControl(0,PUD_DOWN);

    if ((fd = open(filename, O_RDWR)) < 0)
	{
		//ERROR HANDLING: check errno
		printf("Failed to open the i2c bus");
		return;
	}


    
	int addr = 0x32;  //<<<<<The I2C address of the slave
	if (ioctl(fd, I2C_SLAVE, addr) < 0)
	{
		printf("Failed to acquire bus access and/or talk to slave.\n");
		return;
	}

    write(fd,&Totalpower[0], 2);  
    write(fd,&Softstart[0],3);  
   
    //number of bytes = 3
    //What is a soft start?
}





int main()
{
     pthread_t tid1;

     Motorinit();

     pthread_create(&tid1,NULL,Motorcontrol,0);
     //Create and start a new posix thread
     
     pthread_join(tid1,NULL); // add an explanation


     return 0;
}





// The function Motorcontrol runs in a posix thread

void* Motorcontrol(void* param)
{

    while (1)
     {
       write(fd,&MotorHF[0],7);  //forward


       usleep(3000000);
       write(fd,&MotorST[0],7);  //stop


       usleep(3000000);
       write(fd,&MotorHR[0],7);  //reverse

       usleep(3000000);
       write(fd,&MotorST[0],7);   //stop

       usleep(2000000);

      }
}


