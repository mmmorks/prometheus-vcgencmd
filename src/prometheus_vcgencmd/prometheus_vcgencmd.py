#!/usr/bin/env python3

__version__='0.0.0'

import sys
#from subprocess import Popen, PIPE
import subprocess

class Prometheus_Vcgencmd:
    def __init__(self, args=None):
        self.args = args

    def version(self):
        return __version__

    def runcmd(self, cmd):
        #out = subprocess.check_output(cmd.split(), stderr=subprocess.PIPE).decode("utf-8")
        #return out
        return subprocess.check_output(cmd.split(), stderr=subprocess.PIPE).decode("utf-8")

    def run(self, args=None):
        #print('run')
        #cmd = 'vcgencmd measure_temp'
        #proc = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
        #stdout, stderr = proc.communicate()
        #exit_code = proc.wait()
        #print(stdout.decode('utf-8'))

        #cmd = 'vcgencmd measure_temp'
        #out = subprocess.check_output(cmd.split(), stderr=subprocess.PIPE).decode("utf-8")
        #print(out)
        #measure_temp = self.runcmd(cmd)
        #print(measure_temp)

        #-------------------------------------------------------------------------------------

        #vcgencmd_version = self.runcmd('vcgencmd version')
        #vcgencmd_version = self.runcmd('vcgencmd version').rstrip('\n')
        #vcgencmd_version = self.runcmd('vcgencmd version').strip('\n')
        vcgencmd_version = self.runcmd('vcgencmd version').rstrip('\n').splitlines()
        #print(type(str(vcgencmd_version)))
        #print(vcgencmd_version)
        #for line in vcgencmd_version:
        #    print(line)
        version_date = vcgencmd_version[0].strip()
        version_copyright = vcgencmd_version[1]
        version_version = vcgencmd_version[2]
        version_hash = version_version.split()[1]

        #prom = 'vcgencmd{command="version",date="'+str(version_date)+'",copyright="'+str(version_copyright)+'"'
        prom = 'vcgencmd_version{date="'+str(version_date)+'",copyright="'+str(version_copyright)+'",version="'+str(version_hash)+'"} 1'
        print(prom)

        #-------------------------------------------------------------------------------------

        get_camera = self.runcmd('vcgencmd get_camera').rstrip('\n')
        #print(get_camera)
        supported = get_camera.split(' ')[0].split('=')[1]
        detected = get_camera.split(' ')[1].split('=')[1]
        if detected == '0':
            #prom = 'vcgencmd{command="get_camera",supported="'+str(supported)+'"} 0'
            prom = 'vcgencmd_get_camera{supported="'+str(supported)+'"} 0'
        else:
            #prom = 'vcgencmd{command="get_camera",supported="'+str(supported)+'"} 1'
            prom = 'vcgencmd_get_camera{supported="'+str(supported)+'"} 1'

        print(prom)


        #-------------------------------------------------------------------------------------

        get_throttled = self.runcmd('vcgencmd get_throttled').rstrip('\n')
        #print(get_throttled)
        throttledstr = get_throttled.split('=')
        throttled = throttledstr[1]
        #prom = 'vcgencmd{command="get_throttled",bit="'+str(throttled)+'"} 1'
        prom = 'vcgencmd_get_throttled{bit="'+str(throttled)+'"} 1'
        print(prom)



        #-------------------------------------------------------------------------------------

        measure_temp = self.runcmd('vcgencmd measure_temp').rstrip('\n')
        tempscale = measure_temp.split('=')[1]
        temp = tempscale.split("'")[0]
        scale = tempscale.split("'")[1]
        #print(temp, scale)
        #prom = 'vcgencmd{command="measure_temp",scale="'+str(scale)+'"} '+str(temp)
        #prom = 'vcgencmd_measure_temp{scale="'+str(scale)+'"} '+str(temp)
        #vcgencmd_measure_temp{scale="C"} 41.3

        if scale == 'C':
            prom = 'vcgencmd_measure_temp{scale="Celsius"} '+str(temp)
        else:
            prom = 'vcgencmd_measure_temp{scale="'+str(scale)+'"} '+str(temp)
        print(prom)

        #-------------------------------------------------------------------------------------

        measure_volts_core = self.runcmd('vcgencmd measure_volts core').rstrip('\n')
        #print(measure_volts_core)
        measure_voltsV = measure_volts_core.split('=')[1]
        #print(measure_voltsV)
        measure_volts = measure_voltsV.rstrip('V')
        #print(measure_volts)

        #prom = 'vcgencmd_measure_volts_core{scale="V"} '+str(measure_volts)
        prom = 'vcgencmd_measure_volts_core{description="VC4 core voltage"} '+str(measure_volts)
        print(prom)

        #-------------------------------------------------------------------------------------

        measure_volts_sdram_c = self.runcmd('vcgencmd measure_volts sdram_c').rstrip('\n')
        #print(measure_volts_sdram_c)
        measure_voltsV = measure_volts_sdram_c.split('=')[1]
        measure_volts = measure_voltsV.rstrip('V')

        prom = 'vcgencmd_measure_volts_sdram_c{description=""} '+str(measure_volts)
        print(prom)

        #-------------------------------------------------------------------------------------

        measure_volts_sdram_i = self.runcmd('vcgencmd measure_volts sdram_i').rstrip('\n')
        #print(measure_volts_sdram_i)
        measure_voltsV = measure_volts_sdram_i.split('=')[1]
        measure_volts = measure_voltsV.rstrip('V')

        prom = 'vcgencmd_measure_volts_sdram_i{description=""} '+str(measure_volts)
        print(prom)

        #-------------------------------------------------------------------------------------

        measure_volts_sdram_p = self.runcmd('vcgencmd measure_volts sdram_p').rstrip('\n')
        #print(measure_volts_sdram_p)
        measure_voltsV = measure_volts_sdram_p.split('=')[1]
        measure_volts = measure_voltsV.rstrip('V')

        prom = 'vcgencmd_measure_volts_sdram_p{description=""} '+str(measure_volts)
        print(prom)

        #-------------------------------------------------------------------------------------

        display_power = self.runcmd('vcgencmd display_power').rstrip('\n')
        #print(display_power)
        display = display_power.split('=')[1]

        prom = 'vcgencmd_display_power{description="display power state id"} '+str(display)
        print(prom)

        #-------------------------------------------------------------------------------------

        #vcgencmd get_mem arm
        #vcgencmd get_mem gpu

        get_mem_arm = self.runcmd('vcgencmd get_mem arm').rstrip('\n')
        #print(get_mem_arm)
        get_mem_armM = get_mem_arm.split('=')[1]
        mem_arm = get_mem_armM.rstrip('M')

        prom = 'vcgencmd_get_mem_arm{unit="Mbytes"} '+str(mem_arm)
        print(prom)



        get_mem_gpu = self.runcmd('vcgencmd get_mem gpu').rstrip('\n')
        #print(get_mem_gpu)
        get_mem_gpuM = get_mem_gpu.split('=')[1]
        mem_gpu = get_mem_gpuM.rstrip('M')

        prom = 'vcgencmd_get_mem_gpu{unit="Mbytes"} '+str(mem_gpu)
        print(prom)


        #-------------------------------------------------------------------------------------

        #vcgencmd mem_oom

        mem_oom = self.runcmd('vcgencmd mem_oom').rstrip('\n').splitlines()
        #print(mem_oom)

        mem_oom_events = mem_oom[0]
        mem_oom_lifetime = mem_oom[1]
        mem_oom_totaltime = mem_oom[2]
        mem_oom_maxtime = mem_oom[3]

        #prom = 'vcgencmd_get_mem_gpu{unit="Megabytes"} '+str(mem_gpu)
        #print(prom)

        oom_event = mem_oom_events.split(':')[1].strip()
        prom = 'vcgencmd_mem_oom_events{} '+str(oom_event)
        print(prom)

        oom_lifetime = mem_oom_lifetime.split(':')[1]
        #print(oom_lifetime)
        lifetime = oom_lifetime.split()[0].strip()
        lifesize = oom_lifetime.split()[1].strip()

        prom = 'vcgencmd_mem_oom_lifetime{unit="'+str(lifesize)+'"} '+str(lifetime)
        print(prom)

        
        oom_totaltime = mem_oom_totaltime.split(':')[1]
        #print(oom_lifetime)
        ttime = oom_totaltime.split()[0].strip()
        tsize = oom_totaltime.split()[1].strip()

        prom = 'vcgencmd_mem_oom_total_time{unit="'+str(tsize)+'"} '+str(ttime)
        print(prom)


        oom_maxtime = mem_oom_maxtime.split(':')[1]
        #print(oom_lifetime)
        mtime = oom_maxtime.split()[0].strip()
        msize = oom_maxtime.split()[1].strip()

        prom = 'vcgencmd_mem_oom_max_time{unit="'+str(msize)+'"} '+str(mtime)
        print(prom)

        #-------------------------------------------------------------------------------------

        #vcgencmd mem_reloc_stats

        



#vcgencmd vcos [ version | log status ]
#vcgencmd measure_clock [ arm core h264 isp v3d uart pwm emmc pixel vec hdmi dpi ]
#vcgencmd get_lcd_info
#vcgencmd read_ring_osc
#vcgencmd hdmi_timings
#vcgencmd dispmanx_list


def main():
    if sys.argv[1:]:
        if sys.argv[1] == '--version':
            version = Prometheus_Vcgencmd().version()
            print(version)
    else:
        run = Prometheus_Vcgencmd().run()

if __name__ == "__main__":
    sys.exit(main())


