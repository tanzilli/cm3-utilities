#include <asf.h>
#include <stdint.h>
#include <serial.h>
#include <stdio_serial.h>
#include <sam0_usart/usart_serial.h>
#include "adc.h"
#include "YARM_lib.h"

#define LSBFIRST 0
#define MSBFIRST 1
#define DATA_PERIOD 200

//Definizione per le funzioni del main
void menu(void);
void configure_usart(void);
float read_adc(int);

void Event_ExtIntChannel(void);
void Event_ExtIntCallbacks(void);
void Event_Callback(void);

typedef union
{
	uint8_t data[32];
	struct {
		float t;
		float p;
		float h;
		float rssi;
		uint32_t SerialNumber[3];
	} wval;
} SENSOR_DATA_t;

SENSOR_DATA_t sd;
#define SENSOR_DATA_LEN	(sizeof(SENSOR_DATA_t))

uint8_t TxSequence[]={
	0x40,		// 0, Chn 1, Serv 0
	0x50,		// 1, Chn 2, Serv 0
	0x60,		// 2, Chn 3, Serv 0
	0x41,		// 3, Chn 1, Serv 1
	0x51,		// 4, Chn 2, Serv 1
	0x61,		// 5, Chn 3, Serv 1
	0x42,		// 6, Chn 1, Serv 2
	0x52,		// 7, Chn 2, Serv 2
	0x62,		// 8, Chn 3, Serv 2
};
uint8_t seq_idx;

uint32_t TX_ToYarmMobile(void);

volatile uint32_t event_rtc;
volatile uint32_t event_state;

uint32_t txLength;

#define BUF_LENGTH	64
static uint8_t rd_buffer[BUF_LENGTH];
uint32_t	buffer_len;
uint8_t TxPreambleBuffer[]={0x04, 0x70, 0x8E, 0x0A, 0x55, 0x55, 0x10, 0x55, 0x56};

struct adc_module adc_instance;

#define EVENT_EIC_PIN               PIN_PA14A_EIC_EXTINT14
#define EVENT_EIC_MUX               MUX_PA14A_EIC_EXTINT14
#define EVENT_EIC_PINMUX            PINMUX_PA14A_EIC_EXTINT14
#define EVENT_EIC_LINE              14

void configure_usart(void)
{
	static struct usart_module usart_instance;
	struct usart_config config_usart;
	
	usart_get_config_defaults(&config_usart);
	config_usart.baudrate    = 115200;
	config_usart.mux_setting = USART_RX_1_TX_0_XCK_1;
	config_usart.pinmux_pad0 = PINMUX_PA22D_SERCOM5_PAD0;
	config_usart.pinmux_pad1 = PINMUX_PA23D_SERCOM5_PAD1;
	config_usart.pinmux_pad2 = PINMUX_UNUSED;
	config_usart.pinmux_pad3 = PINMUX_UNUSED;
	
	while (usart_init(&usart_instance, SERCOM5, &config_usart) != STATUS_OK);
	stdio_serial_init(&usart_instance, SERCOM5, &config_usart);

	usart_enable(&usart_instance);
}

// ADC_POSITIVE_INPUT_PIN19
// ADC_POSITIVE_INPUT_PIN18
// ADC_POSITIVE_INPUT_PIN0
// ADC_POSITIVE_INPUT_PIN1

float read_adc(int pin)
{
	struct adc_config config_adc;
	uint16_t result;

	adc_get_config_defaults(&config_adc);
	
	config_adc.clock_prescaler				= ADC_CLOCK_PRESCALER_DIV32;
	// Con ADC_REFCTRL_REFSEL_INTVCC0 la VREF sembra essere a 2 volt
	config_adc.reference					= ADC_REFCTRL_REFSEL_INTVCC0;	
	config_adc.positive_input				= pin;
	config_adc.negative_input				= ADC_NEGATIVE_INPUT_GND;
	config_adc.resolution					= ADC_RESOLUTION_12BIT;
	config_adc.accumulate_samples			= ADC_ACCUMULATE_SAMPLES_1024;
	config_adc.divide_result				= ADC_DIVIDE_RESULT_16;
	
	adc_init(&adc_instance, ADC, &config_adc);
	adc_enable(&adc_instance);

	adc_start_conversion(&adc_instance);
	do {
		// Wait for conversion to be done and read out result
	}	while (adc_read(&adc_instance, &result) == STATUS_BUSY);
	adc_disable(&adc_instance);
	return (float)result/2048;
}

#define VREF 3.3

void menu(void) {
	printf("\n\r");
	printf("r) Read ADC\r\n");	
	printf("\r\n");
}

int main (void)
{
	int c;
	uint32_t i;
	
	system_init();
	configure_usart();	
	delay_init();
	
	ioport_init();

	/* BOD33 disabled */
	SUPC->BOD33.reg &= ~SUPC_BOD33_ENABLE;
	
	/* VDDCORE is supplied BUCK converter */
	SUPC->VREG.bit.SEL = SUPC_VREG_SEL_BUCK_Val;

	irq_initialize_vectors();
	cpu_irq_enable();

	/* Enable External Interrupt for Button0 trap */
	// Button_ExtIntChannel();
	// Button_ExtIntCallbacks();
	Event_ExtIntChannel();
	Event_ExtIntCallbacks();
	system_interrupt_enable_global();

	for ( i=0; i<SENSOR_DATA_LEN; i++)
	sd.data[i]=0;

	for ( i=0; i<BUF_LENGTH; i++) {
		rd_buffer[i]=0;
	}


	/* Configure SPI and PowerUp ATA8510 */
	YARM_Init();
	delay_ms(1);
		
	for (;;) {
		printf("\n\rTest CM3-TEST - Ver 0.02\n\r");
		menu();
		c=getchar();


		// Read ADC
	// ADC_POSITIVE_INPUT_PIN19
	// ADC_POSITIVE_INPUT_PIN18
	// ADC_POSITIVE_INPUT_PIN0
	// ADC_POSITIVE_INPUT_PIN1
		
		if (c=='r') {
			printf("Analog 1=%.2f\r\n",read_adc(ADC_POSITIVE_INPUT_PIN19));
			printf("Analog 2=%.2f\r\n",read_adc(ADC_POSITIVE_INPUT_PIN18));
			printf("Analog 3=%.2f\r\n",read_adc(ADC_POSITIVE_INPUT_PIN0));
			printf("Analog 4=%.2f\r\n",read_adc(ADC_POSITIVE_INPUT_PIN1));
		}
	}

}

uint32_t TX_ToYarmMobile(void)
{
	uint32_t i;
	
	YARM_SetIdleMode();
	printf("YARM_SetIdleMode\r\n");
	delay_ms(1);
	
	/* print out YARM state */
	buffer_len = YARM_GetEventBytes( &rd_buffer[0]);
	if ( buffer_len < 0 ) {
		printf( "Errore YARM_GetEventBytes %d\r\n", (int)(buffer_len*-1));
		} else {
		printf( "Reg. GETEVENTBYTES: ");
		for ( i=0; i<buffer_len; i++) {
			printf( "0x%X, ", rd_buffer[i]);
		}
		printf( "\r\n");
	}
	
	buffer_len = YARM_GetVersionFlash( &rd_buffer[0]);
	if ( buffer_len < 0 ) {
		printf( "Errore YARM_GetVersionFlash %d\r\n", (int)(buffer_len*-1));
		} else {
		printf( "Reg. GETVERSIONFLASH: 0x%X\r\n", rd_buffer[0]);
	}
	
	/* print out YARM state */
	buffer_len = YARM_GetEventBytes( &rd_buffer[0]);
	if ( buffer_len < 0 ) {
		printf( "Errore YARM_GetEventBytes %d\r\n", (int)(buffer_len*-1));
		} else {
		printf( "Reg. GETEVENTBYTES: ");
		for ( i=0; i<buffer_len; i++) {
			printf( "0x%X, ", rd_buffer[i]);
		}
		printf( "\r\n");
	}

	//	txLength = TX_ToYarmMobile_PrepareTxData();
	sd.data[0]='A';
	sd.data[1]='B';
	sd.data[2]='C';
	sd.data[3]='D';
	sd.data[4]='E';
	sd.data[5]='F';
	sd.data[6]='G';
	sd.data[7]='H';
	sd.data[8]='I';
	sd.data[9]='L';
	sd.data[10]='M';
	sd.data[11]='N';
	txLength = 12;

	if (txLength==0)
	return 1;
	
	printf("Data to Send [%d]\r\n", (int)txLength);
	
	for ( i=0; i<txLength;i++)
	printf(" 0x%0X, ", sd.data[i]);
	printf("\r\n");
	
	for ( i=0; i<txLength;i++)
		if (sd.data[i]>0x20 || sd.data[i]<0x7f) printf("%c", sd.data[i]); else printf(".");
	
	printf("\r\n");
	
	YARM_SetIdleMode();
	printf("YARM_SetIdleMode\r\n");
	delay_ms(1);
	
	YARM_WriteTxPreamble( YARM_WriteTxPreambleBuffer_LEN, &TxPreambleBuffer[0]);
	printf("YARM_WriteTxPreamble\r\n");
	delay_us(100);

	YARM_WriteTxFifo( txLength, sd.data);
	printf("YARM_WriteTxFifo\r\n");
	delay_us(100);
	
	seq_idx = 0;
	YARM_SetSystemMode( YARM_RF_TXMODE, TxSequence[seq_idx]);
	printf("YARM_SetSystemMode TXMode\n\r");
	delay_ms(250);

	YARM_SetIdleMode();
	printf("YARM_SetIdleMode\r\n");
	delay_ms(1);

	/* print out YARM state */
	buffer_len = YARM_GetEventBytes( &rd_buffer[0]);
	if ( buffer_len < 0 ) {
		printf( "Errore YARM_GetEventBytes %d\r\n", (int)(buffer_len*-1));
		} else {
		printf( "Reg. GETEVENTBYTES: ");
		for ( i=0; i<buffer_len; i++) {
			printf( "0x%X, ", rd_buffer[i]);
		}
		printf( "\r\n");
	}
	
	return 1;
}


//***********************************
// Funzioni di gestione transceiver
//***********************************

void Event_ExtIntChannel(void)
{
	struct extint_chan_conf config_extint_chan;
	extint_chan_get_config_defaults( &config_extint_chan);

	config_extint_chan.gpio_pin           = EVENT_EIC_PIN;
	config_extint_chan.gpio_pin_mux       = EVENT_EIC_MUX;
	config_extint_chan.gpio_pin_pull      = EXTINT_PULL_UP;
	config_extint_chan.detection_criteria = EXTINT_DETECT_FALLING;
	extint_chan_set_config( EVENT_EIC_LINE, &config_extint_chan);
}

void Event_ExtIntCallbacks(void)
{
	extint_register_callback( Event_Callback, EVENT_EIC_LINE, EXTINT_CALLBACK_TYPE_DETECT);
	extint_chan_enable_callback( EVENT_EIC_LINE, EXTINT_CALLBACK_TYPE_DETECT);
}

void Event_Callback(void)
{
	event_state = 1;
}