#include "common.h"

#include "ximc.h"

#include "types.h"
#include "fwprotocol.h"

#include "util.h"
#include "metadata.h"
#include "platform.h"

/*
	Preambule:
	The following structures contain globally accesable data that is devided in some sections
	BCDFlashParamsStr - settings to be stored in flash.
	BCDInfoStr - device manufacturer/id/description info
	BCDRamParamsStr - All misc runtime parameters with global access with exception to the following:
	GETS - Parameters that identify the current device state
	GETC - Currents and voltages of the motor
	GETA - Internal analog and digital states
	RDAN - Analog data
*/

/*
	BCDFlashParamsStr structure contains only data structures that are received/transmitted in protocol commands
	with only exception of CRC code in the end.
	The data inside is intended to be stored in nonvolatile memory and is loaded on startup.
*/
typedef struct /* BCDFlashParamsStr. This structure is for parameters that are saved in nonvolatile memory */
{
	gfwv_cmd_str GFWV; /* Version for check protocol compatibility. */
	sfbs_cmd_str SFBS;
	shom_cmd_str SHOM;
	smov_cmd_str SMOV;
	seng_cmd_str SENG;
	sent_cmd_str SENT;
	spwr_cmd_str SPWR;
	ssec_cmd_str SSEC;
	seds_cmd_str SEDS;
	spid_cmd_str SPID;
	ssni_cmd_str SSNI;
	ssno_cmd_str SSNO;
	seio_cmd_str SEIO;
	sbrk_cmd_str SBRK;
	sctl_cmd_str SCTL;
	sjoy_cmd_str SJOY;
	sctp_cmd_str SCTP;
	surt_cmd_str SURT;
	snmf_cmd_str SNMF;
	snvm_cmd_str SNVM;
	semf_cmd_str SEMF;
	seas_cmd_str SEAS;
	sest_cmd_str SEST;
	uint32_t crc; 

} BCDFlashParamsStr;


/*
 *  BCDInfoStr containes information about device.
 *  It is retrieved in command protocol so packing is required.
 */

typedef struct {

	geti_cmd_str DEVICE_INFO;

} BCDInfoStr;

/*
 *  BCDRamParamsStr contains all globally accessed volatile data, flags, values and so on, except special protocol related structures.
 *  Some portions are retrieved in command protocol so packing is required for them.
 */
typedef struct{

	move_cmd_str MOVE;
	movr_cmd_str MOVR;
	gpos_cmd_str GPOS; /* Holds information about current position. */
	gets_cmd_str GETS; /* Holds current information about device. */
	getc_cmd_str GETC; /* Holds motor currents and voltages. */
	rdan_cmd_str RDAN; /* Analog data in ADC counts */
	dbgr_cmd_str DBGR;

	volatile uint32_t MillisecondCounter; /* Holds milliseconds since firmware start. Updated by SysTick. Must be volatile! */
	volatile uint32_t fReboot; /* A global flag to make main cycle reboot the system */
	volatile uint32_t fClear; /* A global flag to make main cycle clear FRAM */

	int32_t InitADC;		/* Zero current level value for hardware current meter */
	int32_t Isin;			/* Current in sin winding that we must stabilize */
	int32_t Icos;			/* Current in cos winding that we must stabilize */

	uint16_t TicksPerMks;	/* Number of ticks per microsecond. Initializated on startup. */

	uint8_t I2CNumDevices;	/* Number of devices on the I2C bus */
	uint8_t I2CID_COM[I2C_DEVICES_LIMIT]; /* I2C Address for each COM-Port */

	uint8_t GPIOExtState;	/* State */
	uint8_t fPWMAtMax;		/* These flags are set when either winding is at maximum */

	int32_t CurSpeed; /* Desired speed in internal steps per second */
	int32_t CurNomI;

	/*From SMOV */
	uint32_t Accel; /*Internal_steps/s */
	uint32_t Decel; /*Internal_steps/s */

	/* This variable is needed to avoid problems with SPOS, ZERO */
	/* The difference between reported and actual position */
	/* So Position to report = Actual + Shift */
	/* Shift = Reported - Actual */
	/* If we need to set new Shift, in Zero() function, so Actual position */
	/* is Reported as 0, we need to set Shift as -Actual */
	/* Newly stored position should be Actual=NewPos-Shift,  */
	/* so it could be reported as NewPos, if queried just after it was set. */
	int64_t PositionShift;
	/*Encoder shift is needed to avoid problems with encoder position zero command. */
	int64_t EncoderShift;

	/*Moving States */
	uint8_t MovingState;

	/*I2C1 state */
	uint8_t I2C1_STATE;
	/*I2C1_FRAM */
	/*I2C1_1WIRE */
	/*I2C1_IDLE */

} BCDRamParamsStr;

/*
 *  BCDStageParamsStr contains all data about external stage
 */
typedef struct {
	snme_cmd_str SNME;
	ssti_cmd_str SSTI;
	ssts_cmd_str SSTS;
	smti_cmd_str SMTI;
	smts_cmd_str SMTS;
	seni_cmd_str SENI;
	sens_cmd_str SENS;
	shsi_cmd_str SHSI;
	shss_cmd_str SHSS;
	sgri_cmd_str SGRI;
	sgrs_cmd_str SGRS;
	sacc_cmd_str SACC;

} BCDStageParamsStr;

#define READ_STRUCTURE(Name) memcpy(&Name, in_buf + COMMAND_LENGTH, sizeof(Name))

#define WRITE_STRUCTURE(STRUCT) \
		zerofill = 0; \
		crc = CRC16((uint8_t *)&STRUCT, sizeof(STRUCT)); \
		memcpy(out_buf + StartPos, &STRUCT, sizeof(STRUCT)); \
		StartPos += sizeof(STRUCT);

#define S(CODE, STRUCT) \
	case S##CODE##_CMD:\
		READ_STRUCTURE(all->BCD##STRUCT##Params.S##CODE);\
		break;

#define G(CODE, STRUCT) \
	case G##CODE##_CMD: \
		WRITE_STRUCTURE(all->BCD##STRUCT##Params.S##CODE); \
		break

/* a struct that holds all info about our controller (it is saved to file) */
typedef struct
{
	char version[16];
	BCDRamParamsStr BCDRamParams;
	BCDFlashParamsStr BCDFlashParams;
	BCDStageParamsStr BCDStageParams;
	BCDInfoStr BCDInfo;
	/* in microseconds */
	uint64_t last_tick;
	uint32_t serial;
} AllParamsStr;

/* returns random int between "low" and "high" (inclusive) */
int rand_range(int low, int high)
{
	return ((rand() % (high - low + 1)) + low);
}

int sgn(double val)
{
	return (0.0 < val) - (val < 0.0);
}

double ximc_dmin(double a, double b)
{
	return a < b ? a : b;
}

/* Calculate current full position of the virtual engine */
static gets_cmd_str CalculateNewPosition(smov_cmd_str smov,
										   seng_cmd_str seng,
										   gets_cmd_str gets_value,
										   move_cmd_str move,
										   uint64_t last_tick)
{
	uint64_t this_tick;
	get_wallclock_us(&this_tick);
	/* declared as double to have less problems with implicit type conversion */
	double micromult = (1 << (seng.MicrostepMode-1));
	double diff = (this_tick - last_tick)*
				  (smov.Speed + (smov.uSpeed / micromult))/powi(10,6);

	double new_pos = gets_value.CurPosition + gets_value.uCurPosition / micromult;
	double tgt_pos = move.Position + move.uPosition / micromult;
	if ((gets_value.MvCmdSts & MVCMD_NAME_BITS) == MVCMD_RIGHT) {
		new_pos += diff;
	} else if ((gets_value.MvCmdSts & MVCMD_NAME_BITS) == MVCMD_LEFT) {
		new_pos -= diff;
	} else if ((gets_value.MvCmdSts & MVCMD_NAME_BITS) == MVCMD_MOVE ||
			   (gets_value.MvCmdSts & MVCMD_NAME_BITS) == MVCMD_MOVR) {
		new_pos += ximc_dmin(diff, fabs(new_pos - tgt_pos)) * sgn(tgt_pos - new_pos);
		if (new_pos == tgt_pos)
		{
			gets_value.MvCmdSts &= ~MVCMD_RUNNING;
			gets_value.CurSpeed = 0;
			gets_value.uCurSpeed = 0;
		}
	}
	
	gets_value.CurPosition = (uint32_t)(long long)new_pos;		
	gets_value.uCurPosition = (int16_t)((new_pos - (long long)new_pos)*micromult);

	return gets_value;
}


unsigned short CRC16(const uint8_t *pbuf, unsigned short n)
{
	unsigned short crc, i, j, carry_flag, a;
	crc = 0xffff;
	for(i = 0; i < n; i++)
	{
		crc = crc ^ pbuf[i];
		for(j = 0; j < 8; j++)
		{
			a = crc;
			carry_flag = a & 0x0001;
			crc = crc >> 1;
			if ( carry_flag == 1 ) crc = crc ^ 0xa001;
		}
	}
	return crc;
}

/*
	This function is a lookup routine to get additional data length in the packet
	If command is listed in the switch placeholder - it returns corresponding data length.
	If not - it returns zero, which means that no additional data is attached.
*/

static uint16_t GetReadDataSize(uint32_t Command)
{
	uint32_t i;
	for (i = 0; CmdLengths[i].Cmd != 0; i++)
	{
		if (Command == CmdLengths[i].Cmd)
		{
			if (CmdLengths[i].SendBytes == 0)
				return 0;
			else
			{
				/* return bytes that were send to us minus CRC and command code */
				return CmdLengths[i].SendBytes - PROTOCOL_CRC_SIZE - COMMAND_LENGTH;
			}
		}
	}
	return 0;
}

static uint16_t GetWriteDataSize(uint32_t Command)
{
	uint32_t i;
	for (i = 0; CmdLengths[i].Cmd != 0; i++)
	{
		if (Command == CmdLengths[i].Cmd)
		{
			if (CmdLengths[i].ReceiveBytes == 0)
				return 0;
			else
			{
				/* return bytes that were receive to us minus CRC and command code */
				return CmdLengths[i].ReceiveBytes - PROTOCOL_CRC_SIZE - COMMAND_LENGTH;
			}
		}
	}
	return 0;
}

// Struct used for emulationing oscilloscope functionality of ximc. Its 25-long arrays are filled with zeros.
static measurements_t measurements = { .Length = 25 };

/*
	This function gets a command-packet structure and puts response into Array.
	The Array size must be enough to hold any single response.
	The return value is the size of writtendata into Array
 */
static uint16_t GetData(const uint8_t *in_buf, size_t data_size, uint8_t *out_buf,
		AllParamsStr* all)
{
	/* We are going to add data to the Array, so we need a byte counter. */
	/* We also are going to return its value. */
	uint16_t StartPos = 0;
	/* This value will contain the packet CRC16 code to verify its data */
	uint16_t crc;
	int writesize;
	const uint32_t command32 = *((uint32_t*)in_buf);
	int zerofill = 1; /* if true, then return array is filled with zeroes */

	memset(out_buf, 0, PACKET_SIZE); /* remove? */
	/* Each transmit starts with command code */
	memcpy(out_buf, in_buf, COMMAND_LENGTH);
	StartPos += COMMAND_LENGTH;

	/* Update position */
	all->BCDRamParams.GETS = CalculateNewPosition(all->BCDFlashParams.SMOV,
												  all->BCDFlashParams.SENG,
												  all->BCDRamParams.GETS,
												  all->BCDRamParams.MOVE,
												  all->last_tick);
	get_wallclock_us(&all->last_tick);  // TODO: think about adding this function to CalculateNewPosition(...)


	/* data_size does not include command or crc length */
	if (data_size != 0) /* If there is data */
	{
		/* Calculate CRC */
		crc = *((uint16_t*)(in_buf + COMMAND_LENGTH + data_size));

		/* Processing commands with data */
		switch(command32)
		{
			case ASIA_CMD: break;
			case MOVE_CMD:
			{
			   move_cmd_str MoveArr;
			   READ_STRUCTURE(MoveArr);
			   all->BCDRamParams.MOVE.Position = MoveArr.Position;
			   all->BCDRamParams.MOVE.uPosition = MoveArr.uPosition;
			   all->BCDRamParams.GETS.MvCmdSts = MVCMD_MOVE | MVCMD_RUNNING;
			   all->BCDRamParams.GETS.CurSpeed = all->BCDFlashParams.SMOV.Speed;
			   all->BCDRamParams.GETS.uCurSpeed = all->BCDFlashParams.SMOV.uSpeed;
			   break;
			}

			case MOVR_CMD:
			{
			   movr_cmd_str MovrArr;
			   READ_STRUCTURE(MovrArr);
			   all->BCDRamParams.MOVE.Position += MovrArr.DeltaPosition;
			   all->BCDRamParams.MOVE.uPosition += MovrArr.uDeltaPosition;
			   all->BCDRamParams.GETS.MvCmdSts = MVCMD_MOVR | MVCMD_RUNNING;
			   all->BCDRamParams.GETS.CurSpeed = all->BCDFlashParams.SMOV.Speed;
			   all->BCDRamParams.GETS.uCurSpeed = all->BCDFlashParams.SMOV.uSpeed;
			   break;
			}
			case SPOS_CMD:
			{
			   spos_cmd_str PosArr;
			   READ_STRUCTURE(PosArr);
			   if (!(PosArr.PosFlags & SETPOS_IGNORE_POSITION)) {
				   all->BCDRamParams.GETS.CurPosition = PosArr.Position;
				   all->BCDRamParams.GETS.uCurPosition = PosArr.uPosition;
			   }
			   if (!(PosArr.PosFlags & SETPOS_IGNORE_ENCODER))
				   all->BCDRamParams.GETS.EncPosition = PosArr.EncPosition;
			   break;
			}

			S(FBS, Flash);
			S(NMF, Flash);
			S(NVM, Flash);
			S(NME, Stage);
			S(STI, Stage);
			S(STS, Stage);
			S(MTI, Stage);
			S(MTS, Stage);
			S(ENI, Stage);
			S(ENS, Stage);
			S(HSI, Stage);
			S(HSS, Stage);
			S(GRI, Stage);
			S(GRS, Stage);
			S(ACC, Stage);
			S(ENT, Flash);
			S(SEC, Flash);
			S(EDS, Flash);
			S(PID, Flash);
			S(EMF, Flash);
			S(EAS, Flash);
			S(EST, Flash);
			S(HOM, Flash);
			S(MOV, Flash);
			S(ENG, Flash);
			S(URT, Flash);
			S(PWR, Flash);
			S(SNI, Flash);
			S(SNO, Flash);
			S(EIO, Flash);
			S(BRK, Flash);
			S(CTL, Flash);
			S(JOY, Flash);
			S(CTP, Flash);

			default:
			   memcpy(out_buf,"errc",COMMAND_LENGTH);
			   return COMMAND_LENGTH;
		}
		memcpy(out_buf, in_buf, COMMAND_LENGTH);
		return COMMAND_LENGTH;
	}

	/* ----- Processing commands without data ----- // */
	switch (command32)
	{
		case STOP_CMD:
		   all->BCDRamParams.GETS.MvCmdSts = MVCMD_STOP;
		   all->BCDRamParams.GETS.CurSpeed = 0;
		   all->BCDRamParams.GETS.uCurSpeed = 0;
		   break;
		case SSTP_CMD:
		   all->BCDRamParams.GETS.MvCmdSts = MVCMD_SSTP;
		   all->BCDRamParams.GETS.CurSpeed = 0;
		   all->BCDRamParams.GETS.uCurSpeed = 0;
		   break;
		case ZERO_CMD:
		   all->BCDRamParams.GETS.CurPosition = 0;
		   all->BCDRamParams.GETS.uCurPosition = 0;
		   all->BCDRamParams.GETS.EncPosition = 0;
		   all->BCDRamParams.MOVE.Position = 0;
		   all->BCDRamParams.MOVE.uPosition = 0;
		   break;
		case HOME_CMD:
		   all->BCDRamParams.GETS.MvCmdSts = MVCMD_HOME;
		   break;
		case LEFT_CMD:
		   all->BCDRamParams.GETS.MvCmdSts = MVCMD_LEFT | MVCMD_RUNNING;
		   all->BCDRamParams.GETS.CurSpeed = all->BCDFlashParams.SMOV.Speed;
		   all->BCDRamParams.GETS.uCurSpeed = all->BCDFlashParams.SMOV.uSpeed;
		   all->BCDRamParams.GETS.CurSpeed = -all->BCDRamParams.GETS.CurSpeed;
		   all->BCDRamParams.GETS.uCurSpeed = -all->BCDRamParams.GETS.uCurSpeed;
		   break;
		case STMS_CMD: break;
		case GETM_CMD:
			WRITE_STRUCTURE(measurements);
		case RIGT_CMD:
		   all->BCDRamParams.GETS.MvCmdSts = MVCMD_RIGHT | MVCMD_RUNNING;
		   all->BCDRamParams.GETS.CurSpeed = all->BCDFlashParams.SMOV.Speed;
		   all->BCDRamParams.GETS.uCurSpeed = all->BCDFlashParams.SMOV.uSpeed;
		   break;
		case GETS_CMD:
		{
		   /* Let's imagine things */
		   all->BCDRamParams.GETS.Upwr = rand_range(1201, 1210);
		   all->BCDRamParams.GETS.Ipwr = rand_range(3, 9);
		   all->BCDRamParams.GETS.Uusb = rand_range(480, 520);
		   all->BCDRamParams.GETS.Iusb = rand_range(180, 210);
		   all->BCDRamParams.GETS.CurT = 366;
		   WRITE_STRUCTURE(all->BCDRamParams.GETS);
		   break;
	   	}
		case GETC_CMD:
	   	{
		   all->BCDRamParams.GETC.Joy = rand_range(4500, 5000);
		   all->BCDRamParams.GETC.Pot = rand_range(6000, 8000);
		   all->BCDRamParams.GETC.DutyCycle = 200;

		   WRITE_STRUCTURE(all->BCDRamParams.GETC);
		   break;
	   	}
		case RDAN_CMD:
		{
		   all->BCDRamParams.RDAN.R = rand_range(0, 20000);
		   all->BCDRamParams.RDAN.L = rand_range(0, 40000);

		   WRITE_STRUCTURE(all->BCDRamParams.RDAN);
		   break;
	   	}
		case GSER_CMD:
	   	{
		   WRITE_STRUCTURE(all->serial);
		   break;
	   	}
		case GETI_CMD:
	   	{
		   WRITE_STRUCTURE(all->BCDInfo.DEVICE_INFO);
		   break;
	   	}
		case REST_CMD: break;
		case UPDF_CMD: break;
		case CLFR_CMD: break;
		case PWOF_CMD: break;
		case LOFT_CMD: break;
		case SAVE_CMD: break;
		case READ_CMD: break;
		case EESV_CMD: break;
		case EERD_CMD: break;
		case GPOS_CMD: 
		{
			all->BCDRamParams.GPOS.Position    = all->BCDRamParams.GETS.CurPosition;
			all->BCDRamParams.GPOS.uPosition   = all->BCDRamParams.GETS.uCurPosition;
			WRITE_STRUCTURE(all->BCDRamParams.GPOS);
			break;
		}
		case GFWV_CMD: break;
		case GBLV_CMD: break;
		case DBGR_CMD: break;

		G(HOM, Flash);
		G(SNI, Flash);
		G(SNO, Flash);
		G(EIO, Flash);
		G(NMF, Flash);
		G(NVM, Flash);

		G(PID, Flash);
		G(EMF, Flash);
		G(EAS, Flash);
		G(EST, Flash);
		G(EDS, Flash);
		G(ENG, Flash);
		G(MOV, Flash);
		G(FBS, Flash);
		G(ENT, Flash);
		G(URT, Flash);
		G(PWR, Flash);
		G(SEC, Flash);
		G(BRK, Flash);
		G(CTL, Flash);
		G(JOY, Flash);
		G(CTP, Flash);

		G(NME, Stage);
		G(STI, Stage);
		G(STS, Stage);
		G(MTI, Stage);
		G(MTS, Stage);
		G(ENI, Stage);
		G(ENS, Stage);
		G(HSI, Stage);
		G(HSS, Stage);
		G(GRI, Stage);
		G(GRS, Stage);
		G(ACC, Stage);

		default:
		   /* Command length is assumed to be four as it is "errc" size */
		   memcpy(out_buf, "errc", COMMAND_LENGTH);
		   /* We set a flag to indicate errc state
		   BCDRamParams.GETS.Flags |= STATE_ERRC;*/
		   return COMMAND_LENGTH;
	}

	if (zerofill)
	{
		writesize = GetWriteDataSize(command32);
		memset(out_buf + StartPos, 0, writesize);
		crc = CRC16(out_buf + StartPos, writesize);
		StartPos += writesize;
	}

	if (StartPos > COMMAND_LENGTH) /* If data was added */
	{
		memcpy(out_buf + StartPos, &crc, 2); /* Add previously calculated CRC */
		StartPos += 2;
	}
	return StartPos;
}

ssize_t read_port_virtual (device_metadata_t *metadata, void *buf, size_t amount)
{
	if (metadata->virtual_packet_actual + amount > metadata->virtual_packet_size)
	{
		log_error( L"Virtual packet overflow from %d to %d by %d",
				metadata->virtual_packet_actual, metadata->virtual_packet_size, amount);
		return -1;
	}
	else
	{
		memcpy( buf, metadata->virtual_scratchpad + metadata->virtual_packet_actual,
				amount );
		metadata->virtual_packet_actual += amount;

		return (ssize_t)amount;
	}
}

ssize_t write_port_virtual (device_metadata_t *metadata, const void *buf, size_t amount)
{
	AllParamsStr* allParams = (AllParamsStr*)metadata->virtual_state;
	size_t in_data_size = GetReadDataSize(*((uint32_t*)buf));

	/* Process data and save response in scratchpad */
	metadata->virtual_packet_actual = 0;
	metadata->virtual_packet_size = GetData(buf, in_data_size,
			metadata->virtual_scratchpad, allParams);
	if (metadata->virtual_packet_size > VIRTUAL_SCRATCHPAD_SIZE)
	{
		log_error( L"Scratchpad overflow" );
		return -1;
	}
	log_debug( L"Write virtual port in logical %d, out binary %d",
			amount, metadata->virtual_packet_size );

	return amount;
}

void create_empty_state (AllParamsStr* blob, const char* serial)
{
	size_t i;
	BCDFlashParamsStr *bcd = &blob->BCDFlashParams;

	log_debug( L"creating empty state" );
	memset( blob, 0, sizeof(AllParamsStr) );
	strncpy( blob->version, PROTOCOL_VERSION_Q, sizeof(blob->version) );

	/* SFBS settings */
	bcd->SFBS.IPS = 4000;
	bcd->SFBS.FeedbackType = FEEDBACK_NONE;
	bcd->SFBS.FeedbackFlags = 0;

	/* SHOM settings */
	bcd->SHOM.FastHome = 1000;
	bcd->SHOM.uFastHome = 0;
	bcd->SHOM.SlowHome = 20;
	bcd->SHOM.uSlowHome = 0;
	bcd->SHOM.HomeDelta = 500;
	bcd->SHOM.uHomeDelta = 0;
	bcd->SHOM.HomeFlags = HOME_DIR_SECOND | HOME_STOP_FIRST_LIM | HOME_STOP_SECOND_REV;

	/* SMOV settings */
	bcd->SMOV.Speed = 1000;
	bcd->SMOV.uSpeed = 0;
	bcd->SMOV.Accel = 1000;
	bcd->SMOV.Decel = 2000;
	bcd->SMOV.AntiplaySpeed = 50;
	bcd->SMOV.uAntiplaySpeed = 0;
	/* SENG settings */
	bcd->SENG.NomVoltage = 1200;
	bcd->SENG.NomCurrent = 500;
	bcd->SENG.NomSpeed = 5000;
	bcd->SENG.uNomSpeed = 0;
	bcd->SENG.EngineFlags = ENGINE_ACCEL_ON | ENGINE_LIMIT_VOLT | ENGINE_LIMIT_CURR | ENGINE_LIMIT_RPM;
	bcd->SENG.Antiplay = 50;
	bcd->SENG.MicrostepMode = MICROSTEP_MODE_FRAC_256;
	bcd->SENG.StepsPerRev = 200;
	/* SENT settings */
	bcd->SENT.EngineType = ENGINE_TYPE_STEP;
	bcd->SENT.DriverType = DRIVER_TYPE_INTEGRATE;
	/* SPWR settings */
	bcd->SPWR.HoldCurrent = 60;
	bcd->SPWR.CurrReductDelay = 1500;
	bcd->SPWR.PowerOffDelay = 3600;
	bcd->SPWR.CurrentSetTime = 600;
	bcd->SPWR.PowerFlags = POWER_REDUCT_ENABLED;
	/* SSEC settings */
	bcd->SSEC.LowUpwrOff = 800;
	bcd->SSEC.CriticalIpwr = 3000;
	bcd->SSEC.CriticalUpwr = 4000;
	bcd->SSEC.CriticalT = 800;
	bcd->SSEC.CriticalIusb = 450;
	bcd->SSEC.CriticalUusb = 520;
	bcd->SSEC.MinimumUusb = 420;
	bcd->SSEC.Flags = ALARM_ON_DRIVER_OVERHEATING | LOW_UPWR_PROTECTION |
		H_BRIDGE_ALERT | ALARM_ON_BORDERS_SWAP_MISSET;
	/* SEDS settings */
	bcd->SEDS.BorderFlags = BORDER_STOP_LEFT | BORDER_STOP_RIGHT;
	bcd->SEDS.EnderFlags = ENDER_SW1_ACTIVE_LOW | ENDER_SW2_ACTIVE_LOW;
	bcd->SEDS.LeftBorder = -1000;
	bcd->SEDS.uLeftBorder = 0;
	bcd->SEDS.RightBorder = 1000;
	bcd->SEDS.uRightBorder = 0;
	/* SPID settings */
	bcd->SPID.KpU = 300;
	bcd->SPID.KiU = 1000;
	bcd->SPID.KdU = 0;
	/* SEMF settings */
	bcd->SEMF.BackEMFFlags = 0;
	bcd->SEMF.Km = (FLT32) 0.0025;
	bcd->SEMF.L = (FLT32) 0.0054;
	bcd->SEMF.R = (FLT32) 7.4;
	/* SEAS settings */
	bcd->SEAS.stepcloseloop_Kw = 0;
	bcd->SEAS.stepcloseloop_Kp_low = 0;
	bcd->SEAS.stepcloseloop_Kp_high = 0;
	/* SEST settings */
	bcd->SEST.Param1 = 0;
	/* SSNI settings */
	bcd->SSNI.SyncInFlags = 0;
	bcd->SSNI.ClutterTime = 2000;
	bcd->SSNI.Position = 0;
	bcd->SSNI.uPosition = 0;
	bcd->SSNI.Speed = 500;
	bcd->SSNI.uSpeed = 0;
	/* SSNO settings */
	bcd->SSNO.SyncOutFlags = SYNCOUT_ONSTART | SYNCOUT_ONSTOP;
	bcd->SSNO.SyncOutPulseSteps = 100;
	bcd->SSNO.SyncOutPeriod = 2000;
	/* SEIO settings */
	bcd->SEIO.EXTIOSetupFlags = EXTIO_SETUP_OUTPUT;
	bcd->SEIO.EXTIOModeFlags = EXTIO_SETUP_MODE_OUT_OFF;
	/* SBRK settings */
	bcd->SBRK.t1 = 300;
	bcd->SBRK.t2 = 500;
	bcd->SBRK.t3 = 300;
	bcd->SBRK.t4 = 400;
	bcd->SBRK.BrakeFlags = BRAKE_ENG_PWROFF;
	/* SCTL settings */
	for (i = 0; i < 10; i++)
	{
		bcd->SCTL.MaxSpeed[i] = 0;
		bcd->SCTL.uMaxSpeed[i] = 0;
		bcd->SCTL.Timeout[i] = 1000;
	} /* Fix some settings later */
	bcd->SCTL.MaxSpeed[0] =  1;
	bcd->SCTL.MaxSpeed[1] =  10;
	bcd->SCTL.MaxSpeed[2] =  100;
	bcd->SCTL.MaxSpeed[3] =  1000;
	bcd->SCTL.MaxSpeed[4] =  10000;
	bcd->SCTL.Timeout[0] = 200;
	bcd->SCTL.Timeout[1] = 500;
	bcd->SCTL.Timeout[2] = 800;
	bcd->SCTL.Flags = CONTROL_MODE_OFF;
	/* SJOY settings */
	bcd->SJOY.JoyLowEnd = 0;
	bcd->SJOY.JoyCenter = 5000;
	bcd->SJOY.JoyHighEnd = 10000;
	bcd->SJOY.ExpFactor = 100;
	bcd->SJOY.DeadZone = 50;

	/* SCTP settings */
	/* Minimum contrast steps from step motor encoder position, which set
	 * STATE_CTP_ERROR flag. Measured in steps step motor. Range: 0..255 */
	bcd->SCTP.CTPMinError = 8;
	bcd->SCTP.CTPFlags = CTP_ALARM_ON_ERROR;

	/* SURT settings */
	bcd->SURT.Speed = 115200;
	bcd->SURT.UARTSetupFlags = UART_PARITY_BIT_EVEN;

	/* SNAM settings */
	bcd->SNMF.ControllerName[0] = 0;
	bcd->SNMF.CtrlFlags = EEPROM_PRECEDENCE;

	/* GETI setting */
	memcpy(&blob->BCDInfo.DEVICE_INFO.Manufacturer, "XIMC", 4);
	memcpy(&blob->BCDInfo.DEVICE_INFO.ManufacturerId, "SM", 2);
	memcpy(&blob->BCDInfo.DEVICE_INFO.ProductDescription, "XISM-USB", 8);

	/* Serial */
	if (serial)
	{
		if (sscanf(serial, "%u", &blob->serial) != 1)
			serial = 0;
		log_debug( L"Setting existing serial: %u", blob->serial);
	}
}

/* Returns 1 if virtual state is incompatible with sources */
int check_state_version (AllParamsStr* blob)
{
	char file_version[sizeof(blob->version)+1] = { 0 };
	char actual_version[sizeof(blob->version)+1] = { 0 };
	char *tmp;

	memcpy( file_version, blob->version, sizeof(blob->version) );
	memcpy( actual_version, PROTOCOL_VERSION_Q, sizeof(PROTOCOL_VERSION_Q) );

	/* cut major version */
	if ((tmp = strstr( file_version, "." )) != NULL)
		*tmp = 0;
	if ((tmp = strstr( actual_version, "." )) != NULL)
		*tmp = 0;

	log_debug( L"Comparing versions: file %hs and actual %hs", file_version, actual_version );

	return strcmp(file_version, actual_version) != 0;
}

result_t open_port_virtual (device_metadata_t *metadata, const char* virtual_path, const char* serial)
{
	FILE *file;
	AllParamsStr *blob;
	size_t flen;
	int need_create_empty_state = 1;

	if (PACKET_SIZE > VIRTUAL_SCRATCHPAD_SIZE)
	{
		log_system_error( L"not enough scratchpad size" );
		return result_error;
	}


	blob = malloc(sizeof(AllParamsStr));
	if (!blob)
	{
		log_system_error( L"cannot allocate memory" );
		return result_error;
	}

	file = fopen( virtual_path, "rb+" );
	if (file == NULL)
	{
		log_warning( L"no state file, creating" );

		/* Reopen as rw */
		file = fopen( virtual_path, "wb+" );
		if (file == NULL)
		{
			log_system_error( L"can't open virtual device %hs due to: ", virtual_path );
			free( blob );
			return result_error;
		}
	}
	else
	{
		/* Get a file size */
		if (fseek( file, 0, SEEK_END ))
		{
			fclose( file );
			free( blob );
			return result_error;
		}
		flen = (size_t)ftell( file );

		if (flen == sizeof(AllParamsStr))
		{
			/* Read a state from file */
			if (fseek( file, 0, SEEK_SET ))
			{
				fclose( file );
				free( blob );
				return result_error;
			}
			if (fread( blob, sizeof(AllParamsStr), 1, file ) != 1)
			{
				fclose( file );
				free( blob );
				return result_error;
			}

			/* Check state version */
			if (check_state_version( blob ))
			{
				log_warning( L"state file version mismatch, creating new state" );
				need_create_empty_state = 1;
			}
			else
				need_create_empty_state = 0;
		}
		else
		{
			log_warning( L"wrong virtual data file size (expected %d, got %d), creating new state", sizeof(AllParamsStr), flen );
			
			/* truncate the file */
			fclose( file );
			file = fopen( virtual_path, "wb+" );
			if (file == NULL)
			{
				log_system_error( L"can't open virtual device %hs due to: ", virtual_path );
				free( blob );
				return result_error;
			}
		}
	}

	if (need_create_empty_state)
	{
		/* Initialize an empty state */
		create_empty_state( blob, serial );
	}

	/* save metadata */
	metadata->handle = (handle_t)rand();
	metadata->type = dtVirtual;
	metadata->virtual_state = blob;
	metadata->virtual_file = file;
	
	return result_ok;
}

result_t close_port_virtual (device_metadata_t *metadata)
{
	/* Write virtual blob back to state file */
	if (!metadata->virtual_state)
		return result_error;
	
	if (fseek( metadata->virtual_file, 0, SEEK_SET ) != 0 ||
			fwrite( metadata->virtual_state, sizeof(AllParamsStr), 1,
				metadata->virtual_file ) != 1)
	{
		fclose( metadata->virtual_file );
		return result_error;
	}

	/* Close a state file */
	if (fclose( metadata->virtual_file ))
	{
		log_system_error( L"error closing virtual device: " );
		return result_error;
	}

	free( metadata->virtual_state );

	return result_ok;
}

/* vim: ts=4 shiftwidth=4 */
