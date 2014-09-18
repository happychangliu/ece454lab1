# imports

import subprocess
import os
import re

# globals

debug = True
timing_runs = 1
time_out_file = "time.out"
gprof_out_file = "gprof.out"
ls_size_index = 4

# helper functions

def time_make(time_format, opt1, opt2="", opt3="") :
  total_time = 0

  for i in range(0, timing_runs):
    subprocess.check_output(["make", "clean"])
    subprocess.check_output(["/usr/bin/time", "--output=" + time_out_file, "-f", "%" + time_format, "make", "OPT_FLAG1=" + opt1, "OPT_FLAG2=" + opt2, "OPT_FLAG3=" + opt3])

    temp = open(time_out_file, "r")
    total_time += float(temp.read())
    temp.close()

    if debug :
      print "after iteration " + str(i) + " total_time is " + str(total_time)

  return total_time / timing_runs

def time_make_parallel(time_format, make_flag, opt1, opt2="", opt3="") :
  total_time = 0

  for i in range(0, timing_runs):
    subprocess.check_output(["make", "clean"])
    subprocess.check_output(["/usr/bin/time", "--output=" + time_out_file, "-f", "%" + time_format, "make", make_flag, "OPT_FLAG1=" + opt1, "OPT_FLAG2=" + opt2, "OPT_FLAG3=" + opt3])

    temp = open(time_out_file, "r")
    total_time += float(temp.read())
    temp.close()

    if debug :
      print "after iteration " + str(i) + " total_time is " + str(total_time)

  return total_time / timing_runs

def size_make(opt1, opt2="", opt3="") :
  subprocess.check_output(["make", "clean"])
  subprocess.check_output(["make", "OPT_FLAG1=" + opt1, "OPT_FLAG2=" + opt2, "OPT_FLAG3=" + opt3])
  vpr_info = subprocess.check_output(["ls", "-l", "vpr"])

  if debug :
    print "vpr has size of " + vpr_info.split()[ls_size_index] + " bytes"

  return int(vpr_info.split()[ls_size_index])

def time_run(time_format, opt1, opt2="", opt3="") :
  total_time = 0

  for i in range(0, timing_runs):
    subprocess.check_output(["make", "clean"])
    subprocess.check_output(["make", "OPT_FLAG1=" + opt1, "OPT_FLAG2=" + opt2, "OPT_FLAG3=" + opt3])
    subprocess.check_output(["/usr/bin/time", "--output=" + time_out_file, "-f", "%" + time_format, "vpr", "iir1.map4.latren.net", "k4-n10.xml", "place.out", "route.out", "-nodisp", "-place_only", "-seed", "0"])

    temp = open(time_out_file, "r")
    total_time += float(temp.read())
    temp.close()

    if debug :
      print "after iteration " + str(i) + " total_time is " + str(total_time)

  return total_time / timing_runs

def gprof_run(opt1, opt2="", opt3="") :
  subprocess.check_output(["make", "clean"])
  subprocess.check_output(["rm", "-f", "gmon.out", gprof_out_file])
  subprocess.check_output(["make", "OPT_FLAG1=" + opt1, "OPT_FLAG2=" + opt2, "OPT_FLAG3=" + opt3])
  subprocess.check_output(["vpr", "iir1.map4.latren.net", "k4-n10.xml", "place.out", "route.out", "-nodisp", "-place_only", "-seed", "0"])

  temp = subprocess.check_output(["gprof", "vpr", "gmon.out"])
  lindex = [m.start() for m in re.finditer(r"\n",temp)]
  temp = temp[lindex[2]:lindex[9]]

  if debug :
    print temp

  return temp



# Questions

# Q2
def q2() :
  print "Processing Q2"
  f.write("\nQ2\n")

  compile_time = []

  compile_time.append(("gprof ", time_make("U", "-g", "-pg")))
  compile_time.append(("gcov  ", time_make("U", "-g", "-fprofile-arcs", "-ftest-coverage")))
  compile_time.append(("-g    ", time_make("U", "-g")))
  compile_time.append(("-O2   ", time_make("U", "-O2")))
  compile_time.append(("-O3   ", time_make("U", "-O3")))
  compile_time.append(("-Os   ", time_make("U", "-Os")))

  compile_time = sorted(compile_time, key=lambda option: option[1], reverse=True)
  slowest_compilation = compile_time[0]

  for (opt, time) in compile_time:
    print "option %s takes %5.2f seconds which is %.5f times faster than %s" % (opt, time, slowest_compilation[1]/time, slowest_compilation[0])
    f.write("option %s takes %5.2f seconds which is %.5f times faster than %s\n" % (opt, time, slowest_compilation[1]/time, slowest_compilation[0]))

# Q6
def q6() :
  print "Processing Q6"
  f.write("\nQ6\n")

  parallel_compile_time = []

  parallel_compile_time.append(("1", time_make_parallel("e", "--jobs=1", "-O3")))
  parallel_compile_time.append(("2", time_make_parallel("e", "--jobs=2", "-O3")))
  parallel_compile_time.append(("4", time_make_parallel("e", "--jobs=4", "-O3")))
  parallel_compile_time.append(("8", time_make_parallel("e", "--jobs=8", "-O3")))

  for (opt, time) in parallel_compile_time:
    print "parallel compilation using %s processes takes %5.2f seconds which is %.5f times faster than using %s processes" % (opt, time, parallel_compile_time[0][1]/time, parallel_compile_time[0][0])
    f.write("parallel compilation using %s processes takes %5.2f seconds which is %.5f times faster than using %s processes\n" % (opt, time, parallel_compile_time[0][1]/time, parallel_compile_time[0][0]))

# Q8
def q8() :
  print "Processing Q8"
  f.write("\nQ8\n")

  compile_size = []

  compile_size.append(("gprof ", size_make("-g", "-pg")))
  compile_size.append(("gcov  ", size_make("-g", "-fprofile-arcs", "-ftest-coverage")))
  compile_size.append(("-g    ", size_make("-g")))
  compile_size.append(("-O2   ", size_make("-O2")))
  compile_size.append(("-O3   ", size_make("-O3")))
  compile_size.append(("-Os   ", size_make("-Os")))

  compile_size = sorted(compile_size, key=lambda option: option[1])
  smallest_compilation = compile_size[0]

  for (opt, size) in compile_size:
    print "option %s takes %7d bytes which is %.5f times bigger than %s" % (opt, size, float(size)/smallest_compilation[1], smallest_compilation[0])
    f.write("option %s takes %7d bytes which is %.5f times bigger than %s\n" % (opt, size, float(size)/smallest_compilation[1], smallest_compilation[0]))

# Q12
def q12() :
  print "Processing Q12"
  f.write("\nQ12\n")

  run_time = []

  run_time.append(("gprof ", time_run("U", "-g", "-pg")))
  run_time.append(("gcov  ", time_run("U", "-g", "-fprofile-arcs", "-ftest-coverage")))
  run_time.append(("-g    ", time_run("U", "-g")))
  run_time.append(("-O2   ", time_run("U", "-O2")))
  run_time.append(("-O3   ", time_run("U", "-O3")))
  run_time.append(("-Os   ", time_run("U", "-Os")))

  run_time = sorted(run_time, key=lambda option: option[1], reverse=True)
  slowest_run = run_time[0]

  for (opt, time) in run_time :
    print "option %s takes %5.2f seconds which is %.5f times faster than %s" % (opt, time, slowest_run[1]/time, slowest_run[0])
    f.write("option %s takes %5.2f seconds which is %.5f times faster than %s\n" % (opt, time, slowest_run[1]/time, slowest_run[0]))

# Q16
def q16() :
  print "Processing Q16"
  f.write("\nQ16\n")

  run_time = []

  run_time.append(("-g  ", gprof_run("-g", "-pg")))
  run_time.append(("-O2 ", gprof_run("-O2", "-pg")))
  run_time.append(("-O3 ", gprof_run("-O3", "-pg")))

  for (opt, profile) in run_time :
    print "profiling with gprof using option %s gave the results:\n %s" % (opt, profile)
    f.write("profiling with gprof using option %s gave the results:\n %s\n" % (opt, profile))

# Q19
def q19() :
  print "Processing Q19"
  f.write("\nQ19\n")

  asm_count = []

  # numbers are counted manually
  asm_count.append(("-g  ", 551))
  asm_count.append(("-O3 ", 221))

  asm_count = sorted(asm_count, key=lambda option: option[1], reverse=True)
  largest_asm = asm_count[0]

  for (opt, count) in asm_count :
    print "option %s compiles update_bb() to %d lines of instructions in ASM which is a reduction of %.5f compared to %s" % (opt, count, float(largest_asm[1])/count, largest_asm[0])
    f.write("option %s compiles update_bb() to %d lines of instructions in ASM which is a reduction of %.5f compared to %s" % (opt, count, float(largest_asm[1])/count, largest_asm[0]))

# main

f = open("log.txt", "w")

# q2()
# q6()
# q8()
# q12()
# q16()
q19()

# clean up

f.close()

