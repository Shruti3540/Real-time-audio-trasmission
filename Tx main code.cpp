#include "project.h"
#include "audio_clip.h"
#include "Sapphire.h"
#include "Apt.h"

#define DELAY_US_PER_BYTE 520
#define BUTTON_DEBOUNCE_MS 200

int main(void)
{
    CyGlobalIntEnable;
    UART_Start();
    UART_ClearTxBuffer();
    UART_ClearRxBuffer();

    uint8_t state = 0;  // 0: Song1, 1: Song2, 2: Song3, 3: Silent
    uint8_t prev_button = 1;

    for (;;)
    {
        // Wait for button press (toggle state)
        uint8_t button = Button_Read();
        if (button == 0 && prev_button == 1)
        {
            state = (state + 1) % 4;  // Cycle through 0 to 3
            CyDelay(BUTTON_DEBOUNCE_MS);
        }
        prev_button = button;

        // Loop the selected song
        switch (state)
        {
            case 0:  // Play audio_clip in loop
                for (int i = 0; i < audio_clip_len; i++)
                {
                    if (Button_Read() == 0) break;  // Exit on button press
                    while (!(UART_ReadTxStatus() & UART_TX_STS_FIFO_NOT_FULL));
                    UART_WriteTxData(audio_clip[i]);
                    CyDelayUs(DELAY_US_PER_BYTE);
                }
                break;

            case 1:  // Play Sapphire in loop
                for (int i = 0; i < Sapphire_len; i++)
                {
                    if (Button_Read() == 0) break;
                    while (!(UART_ReadTxStatus() & UART_TX_STS_FIFO_NOT_FULL));
                    UART_WriteTxData(Sapphire[i]);
                    CyDelayUs(DELAY_US_PER_BYTE);
                }
                break;

            case 2:  // Play Apt in loop
                for (int i = 0; i < Apt_len; i++)
                {
                    if (Button_Read() == 0) break;
                    while (!(UART_ReadTxStatus() & UART_TX_STS_FIFO_NOT_FULL));
                    UART_WriteTxData(Apt[i]);
                    CyDelayUs(DELAY_US_PER_BYTE);
                }
                break;

            case 3:  // Silent mode
                CyDelay(10);
                break;
        }
    }
}