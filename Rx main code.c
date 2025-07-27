#include "project.h" 
#include "stdio.h"
CY_ISR(my_isr){
    Pin_1_Write(1);
    uint8 var;
    var = UART_GetChar();
    UART_PutChar(var);
    isr_1_ClearPending();
}
int main(void)
{
   CyGlobalIntEnable;
    UART_Start();
    isr_1_StartEx(my_isr);
    while(1){}
}