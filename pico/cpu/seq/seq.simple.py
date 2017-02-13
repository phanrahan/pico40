def Sequencer( n, site=None ):

    site = make_site(site)

    # A = COUNT
    # B = VEC
    # C = LOAD
    expr = '(~C & A) | (C & B)'

    def counter(x, y, s, e):
		# [VEC, LOAD] -> inc.O
		ci = None
		if y % 2 == 0:
			ci = True if y == 0 else 'CIN'
		co = None
		if y % 2 == 1 and y != n-1:
			co = 'COUT'
		#print x, y, s, e, ci, co
		return Counter1( expr1=expr, cin=ci, cout=co, o=True, site=s, elem=e )

    c = flip( flat( CarryChain( coln( counter, n, site ) ) ) )

    # A = LOAD
    # B = INCR
    inc = LUT2('~A & B', site=site.delta(0,n/2) )
    wire(inc, c.CIN)

    # U, I, L
    incI = inc.I[0]
    I = [incI[1], c.I[0], [incI[0], c.I[1]]]

    return Module( I, c.O, ce=c.CE )

