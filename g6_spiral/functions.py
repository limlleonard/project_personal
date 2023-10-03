def get_input():
  while True:
    ip1=input('Give the number of the teeth (20-80): ')
    try:
      n_teeth=int(ip1)
      if n_teeth>19 and n_teeth<81: break
    except: pass
  while True:
    ip2=input(f'Give the relative radius of the drawing point (1-{n_teeth//6}): ')
    try:
      r3=int(ip2)
      if r3>0 and r3<=n_teeth: break
    except: pass
  return n_teeth, r3