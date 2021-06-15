#!/usr/bin/env python3

__version__='1.0.0'

import sys
import subprocess

try:
    subprocess.check_output("vcgencmd")
except Exception:
    raise ImportError('command not found: vcgencmd. try apt install libraspberrypi-bin')


class Prometheus_Vcgencmd:

    def version(self):
        return __version__

    def runcmd(self, cmd):
        return subprocess.check_output(cmd.split(), stderr=subprocess.PIPE).decode("utf-8")

    def stdout(self):
        promList = self.promList()
        for i in promList:
            print(i)

    def promList(self):
        promList=[]

        #-------------------------------------------------------------------------------------
        #vcgencmd_info

        prom = 'vcgencmd_info{version="'+str(__version__)+'"} 1'
        promList.append(prom)

        #-------------------------------------------------------------------------------------
        #vcgencmd version

        try:
            vcgencmd_version = self.runcmd('vcgencmd version').rstrip('\n').splitlines()
            version_date = vcgencmd_version[0].strip()
            version_copyright = vcgencmd_version[1]
            version_version = vcgencmd_version[2]
            version_hash = version_version.split()[1]
            prom = 'vcgencmd_version{date="'+str(version_date)+'",copyright="'+str(version_copyright)+'",version="'+str(version_hash)+'"} 1'
            promList.append(prom)
        except subprocess.CalledProcessError as e:
            e = 'VCHI initialization failed'
            prom = 'vcgencmd_version_error{error="'+str(e)+'"} 0'
            promList.append(prom)

        #-------------------------------------------------------------------------------------
        #vcgencmd get_camera

        try:
            get_camera = self.runcmd('vcgencmd get_camera').rstrip('\n')
            supported = get_camera.split(' ')[0].split('=')[1]
            detected = get_camera.split(' ')[1].split('=')[1]
            if detected == '0':
                prom = 'vcgencmd_get_camera{supported="'+str(supported)+'"} 0'
            else:
                prom = 'vcgencmd_get_camera{supported="'+str(supported)+'"} 1'

            promList.append(prom)
        except subprocess.CalledProcessError as e:
            e = 'VCHI initialization failed'
            prom = 'vcgencmd_get_camera_error{error="'+str(e)+'"} 0'
            promList.append(prom)

        #-------------------------------------------------------------------------------------
        #vcgencmd get_throttled

        try:
            get_throttled = self.runcmd('vcgencmd get_throttled').rstrip('\n')
            throttledstr = get_throttled.split('=')
            throttled = throttledstr[1]
            prom = 'vcgencmd_get_throttled{bit="'+str(throttled)+'"} 1'
            promList.append(prom)
        except subprocess.CalledProcessError as e:
            e = 'VCHI initialization failed'
            prom = 'vcgencmd_get_throttled_error{error="'+str(e)+'"} 0'
            promList.append(prom)


        #-------------------------------------------------------------------------------------
        #vcgencmd measure_temp

        try:
            measure_temp = self.runcmd('vcgencmd measure_temp').rstrip('\n')
            tempscale = measure_temp.split('=')[1]
            temp = tempscale.split("'")[0]
            scale = tempscale.split("'")[1]

            if scale == 'C':
                prom = 'vcgencmd_measure_temp{scale="Celsius"} '+str(temp)
            else:
                prom = 'vcgencmd_measure_temp{scale="'+str(scale)+'"} '+str(temp)

            promList.append(prom)
        except subprocess.CalledProcessError as e:
            e = 'VCHI initialization failed'
            prom = 'vcgencmd_measure_temp_error{error="'+str(e)+'"} 0'
            promList.append(prom)

        #-------------------------------------------------------------------------------------
        #vcgencmd measure_volts core

        try:
            measure_volts_core = self.runcmd('vcgencmd measure_volts core').rstrip('\n')
            measure_voltsV = measure_volts_core.split('=')[1]
            measure_volts = measure_voltsV.rstrip('V')
            prom = 'vcgencmd_measure_volts_core{description="VC4 core voltage"} '+str(measure_volts)
            promList.append(prom)
        except subprocess.CalledProcessError as e:
            e = 'VCHI initialization failed'
            prom = 'vcgencmd_measure_volts_core_error{error="'+str(e)+'"} 0'
            promList.append(prom)

        #-------------------------------------------------------------------------------------
        #vcgencmd measure_volts sdram_c

        try:
            measure_volts_sdram_c = self.runcmd('vcgencmd measure_volts sdram_c').rstrip('\n')
            measure_voltsV = measure_volts_sdram_c.split('=')[1]
            measure_volts = measure_voltsV.rstrip('V')
            prom = 'vcgencmd_measure_volts_sdram_c{description=""} '+str(measure_volts)
            promList.append(prom)
        except subprocess.CalledProcessError as e:
            e = 'VCHI initialization failed'
            prom = 'vcgencmd_measure_volts_sdram_c_error{error="'+str(e)+'"} 0'
            promList.append(prom)

        #-------------------------------------------------------------------------------------
        #vcgencmd measure_volts sdram_i

        try:
            measure_volts_sdram_i = self.runcmd('vcgencmd measure_volts sdram_i').rstrip('\n')
            measure_voltsV = measure_volts_sdram_i.split('=')[1]
            measure_volts = measure_voltsV.rstrip('V')
            prom = 'vcgencmd_measure_volts_sdram_i{description=""} '+str(measure_volts)
            promList.append(prom)
        except subprocess.CalledProcessError as e:
            e = 'VCHI initialization failed'
            prom = 'vcgencmd_measure_volts_sdram_i_error{error="'+str(e)+'"} 0'
            promList.append(prom)

        #-------------------------------------------------------------------------------------
        #vcgencmd measure_volts sdram_p

        try:
            measure_volts_sdram_p = self.runcmd('vcgencmd measure_volts sdram_p').rstrip('\n')
            measure_voltsV = measure_volts_sdram_p.split('=')[1]
            measure_volts = measure_voltsV.rstrip('V')
            prom = 'vcgencmd_measure_volts_sdram_p{description=""} '+str(measure_volts)
            promList.append(prom)
        except subprocess.CalledProcessError as e:
            e = 'VCHI initialization failed'
            prom = 'vcgencmd_measure_volts_sdram_p_error{error="'+str(e)+'"} 0'
            promList.append(prom)

        #-------------------------------------------------------------------------------------
        #vcgencmd display_power

        try:
            display_power = self.runcmd('vcgencmd display_power').rstrip('\n')
            display = display_power.split('=')[1]
            prom = 'vcgencmd_display_power{description="display power state id"} '+str(display)
            promList.append(prom)
        except subprocess.CalledProcessError as e:
            e = 'VCHI initialization failed'
            prom = 'vcgencmd_display_power_error{error="'+str(e)+'"} 0'
            promList.append(prom)

        #-------------------------------------------------------------------------------------
        #vcgencmd get_mem arm
        #vcgencmd get_mem gpu

        try:
            get_mem_arm = self.runcmd('vcgencmd get_mem arm').rstrip('\n')
            get_mem_armM = get_mem_arm.split('=')[1]
            mem_arm = get_mem_armM.rstrip('M')
            prom = 'vcgencmd_get_mem_arm{unit="Mbytes"} '+str(mem_arm)
            promList.append(prom)
        except subprocess.CalledProcessError as e:
            e = 'VCHI initialization failed'
            prom = 'vcgencmd_get_mem_arm_error{error="'+str(e)+'"} 0'
            promList.append(prom)


        try:
            get_mem_gpu = self.runcmd('vcgencmd get_mem gpu').rstrip('\n')
            get_mem_gpuM = get_mem_gpu.split('=')[1]
            mem_gpu = get_mem_gpuM.rstrip('M')
            prom = 'vcgencmd_get_mem_gpu{unit="Mbytes"} '+str(mem_gpu)
            promList.append(prom)
        except subprocess.CalledProcessError as e:
            e = 'VCHI initialization failed'
            prom = 'vcgencmd_get_mem_gpu_error{error="'+str(e)+'"} 0'
            promList.append(prom)


        #-------------------------------------------------------------------------------------
        #vcgencmd mem_oom

        try:
            mem_oom = self.runcmd('vcgencmd mem_oom').rstrip('\n').splitlines()

            mem_oom_events = mem_oom[0]
            mem_oom_lifetime = mem_oom[1]
            mem_oom_totaltime = mem_oom[2]
            mem_oom_maxtime = mem_oom[3]
            oom_event = mem_oom_events.split(':')[1].strip()
            prom = 'vcgencmd_mem_oom_events{} '+str(oom_event)
            promList.append(prom)

            oom_lifetime = mem_oom_lifetime.split(':')[1]
            lifetime = oom_lifetime.split()[0].strip()
            lifesize = oom_lifetime.split()[1].strip()

            prom = 'vcgencmd_mem_oom_lifetime{unit="'+str(lifesize)+'"} '+str(lifetime)
            promList.append(prom)

            oom_totaltime = mem_oom_totaltime.split(':')[1]
            ttime = oom_totaltime.split()[0].strip()
            tsize = oom_totaltime.split()[1].strip()

            prom = 'vcgencmd_mem_oom_total_time{unit="'+str(tsize)+'"} '+str(ttime)
            promList.append(prom)


            oom_maxtime = mem_oom_maxtime.split(':')[1]
            mtime = oom_maxtime.split()[0].strip()
            msize = oom_maxtime.split()[1].strip()

            prom = 'vcgencmd_mem_oom_max_time{unit="'+str(msize)+'"} '+str(mtime)
            promList.append(prom)
        except subprocess.CalledProcessError as e:
            e = 'VCHI initialization failed'
            prom = 'vcgencmd_mem_oom_error{error="'+str(e)+'"} 0'
            promList.append(prom)


        #-------------------------------------------------------------------------------------
        #vcgencmd mem_reloc_stats

        try:
            mem_reloc_stats = self.runcmd('vcgencmd mem_reloc_stats').rstrip('\n').splitlines()

            alloc_failures = mem_reloc_stats[0].split(':')[1].strip()
            compactions = mem_reloc_stats[1].split(':')[1].strip()
            legacy_block_fails = mem_reloc_stats[2].split(':')[1].strip()

            prom = 'vcgencmd_mem_reloc_stats_alloc_failures{} '+str(alloc_failures)
            promList.append(prom)

            prom = 'vcgencmd_mem_reloc_stats_compactions{} '+str(compactions)
            promList.append(prom)

            prom = 'vcgencmd_mem_reloc_stats_legacy_block_fails{} '+str(legacy_block_fails)
            promList.append(prom)
        except subprocess.CalledProcessError as e:
            e = 'VCHI initialization failed'
            prom = 'vcgencmd_mem_reloc_stats_error{error="'+str(e)+'"} 0'
            promList.append(prom)


        #-------------------------------------------------------------------------------------
        #vcgencmd measure_clock ( arm core h264 isp v3d uart pwm emmc pixel vec hdmi dpi )

        for clock in ('arm','core','h264','isp','v3d','uart','pwm','emmc','pixel','vec','hdmi','dpi'):
            try:
                out = self.runcmd('vcgencmd measure_clock ' + str(clock) ).rstrip('\n')
                val0 = out.split('=')[0].strip()
                val1 = out.split('=')[1].strip()
                prom = 'vcgencmd_measure_clock_'+str(clock)+'{unit="'+str(val0)+'"} '+str(val1)
                promList.append(prom)
            except subprocess.CalledProcessError as e:
                e = 'VCHI initialization failed'
                prom = 'vcgencmd_measure_clock_'+str(clock)+'_error{error="'+str(e)+'"} 0'
                promList.append(prom)


        #-------------------------------------------------------------------------------------
        #vcgencmd get_lcd_info

        try:
            get_lcd_info = self.runcmd('vcgencmd get_lcd_info').rstrip('\n')
            prom = 'vcgencmd_get_lcd_info{info="'+str(get_lcd_info)+'"} 0'
            promList.append(prom)
        except subprocess.CalledProcessError as e:
            e = 'VCHI initialization failed'
            prom = 'vcgencmd_get_lcd_info_error{error="'+str(e)+'"} 0'
            promList.append(prom)

        #-------------------------------------------------------------------------------------
        #vcgencmd hdmi_timings

        try:
            hdmi_timings = self.runcmd('vcgencmd hdmi_timings').rstrip('\n').split('=')[1]
            prom = 'vcgencmd_hdmi_timings{info="'+str(hdmi_timings)+'"} 1'
            promList.append(prom)
        except subprocess.CalledProcessError as e:
            e = 'VCHI initialization failed'
            prom = 'vcgencmd_hdmi_timings_error{error="'+str(e)+'"} 0'
            promList.append(prom)

        #-------------------------------------------------------------------------------------
        #vcgencmd read_ring_osc
        #read_ring_osc(2)=2.203MHz (@0.8500V) (43.8'C)

        try:
            read_ring_osc = self.runcmd('vcgencmd read_ring_osc').rstrip('\n')
            val0 = read_ring_osc.split('=')[0]
            val1 = read_ring_osc.split('=')[1]

            rrspeed = val1.split()[0]
            rrvolts = val1.split()[1]
            rrtmp = val1.split()[2]

            rspeed = rrspeed.rstrip('MHz').strip()
            prom = 'vcgencmd_read_ring_osc_speed{unit="MHz"} ' +str(rspeed)
            promList.append(prom)

            rvolts = rrvolts.lstrip('(@')
            rvolts = rvolts.rstrip('V)')
            prom = 'vcgencmd_read_ring_osc_volts{unit="Volts"} ' +str(rvolts)
            promList.append(prom)

            rtmp = rrtmp.lstrip('(')
            rtmp = rtmp.rstrip(')')
            rtmp_n = rtmp.split("'")[0]
            prom = 'vcgencmd_read_ring_osc_temperature{scale="Celsius"} ' +str(rtmp_n)
            promList.append(prom)
        except subprocess.CalledProcessError as e:
            e = 'VCHI initialization failed'
            prom = 'vcgencmd_read_ring_osc_error{error="'+str(e)+'"} 0'
            promList.append(prom)

        return promList

#vcgencmd vcos [ version | log status ]
#vcgencmd dispmanx_list

def main():
    if sys.argv[1:]:
        if sys.argv[1] == '--version':
            version = Prometheus_Vcgencmd().version()
            print(version)
    else:
        stdout = Prometheus_Vcgencmd().stdout()

if __name__ == "__main__":
    sys.exit(main())


