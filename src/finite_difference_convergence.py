import numpy as np
import matplotlib.pyplot as plt

#default float type can be overridden by the command line argument
# Float = np.longdouble
# Float = np.float64
Float = np.float32

def fun(x: Float) -> Float:
	return np.sin(Float(1.0)/x)

def fp_exact(x: Float) -> Float:
	r = Float(1.0)/x
	return -r*r*np.cos(r)

def fp_forward1(a: Float, h: Float, f) -> Float:
	return (f(a+h)-f(a))/h

def fp_backward1(a: Float, h: Float, f) -> Float:
	return (f(a)-f(a-h))/h

def fp_center2(a: Float, h: Float, f) -> Float:
	return (f(a+h)-f(a-h))/(Float(2.0)*h)

def fp_forward2(a: Float, h: Float, f) -> Float:
	return (Float(-3.0)*f(a)+Float(4.0)*f(a+h)-f(a+Float(2.0)*h)) / (Float(2.0)*h)


def main(A=1.0,N=10,B=10.0):
	a = Float(A)
	h = [Float(B)**(-n) for n in range(N)]
	
	#compute numerical derivatives at x=a with various schemes and step sizes
	fp_f1_v = [fp_forward1(a,h[n],fun)  for n in range(N)]
	fp_b1_v = [fp_backward1(a,h[n],fun) for n in range(N)]
	fp_c2_v = [fp_center2(a,h[n],fun)   for n in range(N)]
	fp_f2_v = [fp_forward2(a,h[n],fun)  for n in range(N)]

	#compute the error in the numerical derivatives
	exact = fp_exact(a)
	fp_f1_e = [abs(exact - fp_f1_v[n]) for n in range(N)]
	fp_b1_e = [abs(exact - fp_b1_v[n]) for n in range(N)]
	fp_c2_e = [abs(exact - fp_c2_v[n]) for n in range(N)]
	fp_f2_e = [abs(exact - fp_f2_v[n]) for n in range(N)]

	#print table of values
	hdr = f"{'h':>12} {'Forward1':>14} {'Backward1':>14} {'Center2':>14} {'Forward2':>14}"
	sep = "-" * len(hdr)
	print("Numerical Derivative Values")
	print(sep)
	print(hdr)
	print(sep)
	for n in range(N):
		print(f"{h[n]:12.2e} {fp_f1_v[n]:14.8f} {fp_b1_v[n]:14.8f} {fp_c2_v[n]:14.8f} {fp_f2_v[n]:14.8f}")
	print(sep)

	#print table of errors
	print("\nNumerical Derivate Errors")
	print(sep)
	print(hdr)
	print(sep)
	for n in range(N):
		print(f"{h[n]:12.2e} {fp_f1_e[n]:14.2e} {fp_b1_e[n]:14.2e} {fp_c2_e[n]:14.2e} {fp_f2_e[n]:14.2e}")
	print(sep)

	#plot log10(h) vs log10(err)
	h_plot = np.array(h, dtype=np.longdouble)
	errors = {
		"Forward1  " : np.array(fp_f1_e, dtype=np.longdouble),
		"Backward1 " : np.array(fp_b1_e, dtype=np.longdouble),
		"Center2   " : np.array(fp_c2_e, dtype=np.longdouble),
		"Forward2  " : np.array(fp_f2_e, dtype=np.longdouble)
	}

	mkr = ['o', 'x', 'v', 's']
	sty = ['-', '--', '-.', ':']
	idx=0;

	fig, (ax1,ax2) = plt.subplots(2,1,figsize=(15,8))
	for label, err in errors.items():
		ax1.loglog(h, err, marker=mkr[idx], linestyle=sty[idx], label=label)
		idx+=1

	ax1.set_xticks(h)
	ax1.set_xlabel("Step size h")
	ax1.set_ylabel("Absolute error")
	ax1.set_title(f"Finite difference errors in np.{np.dtype(Float)} precision")
	ax1.legend()
	ax1.grid(True, which="both", linestyle="--", alpha=0.5)

	#plot the function zoomed into (a,f(a))
	x_plot = np.linspace(np.longdouble(min(h)), np.longdouble(2), 10000, dtype=np.longdouble)
	y_plot = fun(x_plot);

	ax2.plot(x_plot,y_plot)
	ax2.plot(a,fun(a),'ok')

	plt.tight_layout()
	plt.show()

if __name__ == '__main__':
	import sys
	a = float(sys.argv[1]) if len(sys.argv) > 1 else 2.0
	N = int(sys.argv[2])   if len(sys.argv) > 2 else 15
	types = {'float16': np.float16, 'half': np.float16,
			 'float32': np.float32, 'float': np.float32,
			 'float64': np.float64, 'double': np.float64,
			 'longdouble': np.longdouble}
	if len(sys.argv) > 3:
		if sys.argv[3] not in types:
			print(f"Unknown type '{sys.argv[3]}'. Choose from: {', '.join(types)}")
			sys.exit(1)
		# set the global Float type
		Float = types[sys.argv[3]]
	
	B = float(sys.argv[4]) if len(sys.argv) > 4 else 10.0

	# call the main function
	main(a,N,B)