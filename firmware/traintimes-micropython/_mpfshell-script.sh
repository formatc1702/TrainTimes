file=$1
cmd=$2
ext=.py

# Compile?
if [[ $cmd == *"c"* ]]; then
  if [[ $cmd != *"r"* ]]; then
    echo ⚙ Compile!
    /Users/daniel/Documents/Development/2_Utilities/ESP8266/Firmware/micropython-1.8.7/mpy-cross/mpy-cross $file$ext
  fi
  ext=.mpy
fi

# Remove?
if [[ $cmd == *"r"* ]]; then
  echo ❌ Remove!
  cmd_rm="rm $file$ext;"
else
  # echo Do not remove.
  cmd_rm=""
fi

# Upload?
if [[ $cmd == *"u"* ]]; then
  echo 🔼 Upload!
  cmd_up="put $file$ext;"
else
  # echo Do not upload.
  cmd_up=""
fi

# Execute?
if [[ $cmd == *"x"* ]]; then
  echo ✅ Execute!
  cmd_exec="exec import $file;"
else
  # echo Do not execute.
  cmd_exec=""
fi

# Upload!
cmd_full="-n -c open tty.SLAB_USBtoUART; $cmd_rm $cmd_up ls; $cmd_exec close"
#echo File: $file$ext
#echo Cmd: $cmd
#echo $cmd_full
mpfshell $cmd_full

# Move .mpy file
if [[ $cmd == *"c"* && $cmd != *"r"* ]]; then
  if [[ $cmd != *"r"* ]]; then
    mv $file$ext _mpy/$file$ext
  fi
fi
