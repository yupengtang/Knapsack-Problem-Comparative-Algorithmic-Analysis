from SA import SA
from Knapsack_BnB import BnB
from Approx import Approx
from HillClimbing import HCOnce
import argparse




if __name__=="__main__":
	parser = argparse.ArgumentParser(prog='CSE6140',
                    description='This program experiment different algorithms to solve Knapsack Problem',
                    epilog='Follow the rule to input parameters')
	parser.add_argument('-inst','--inst')
	parser.add_argument('-alg','--alg',choices=['BnB','Approx','HC','SA'])
	parser.add_argument('-time','--time',type=int)
	parser.add_argument('-seed','--seed',type=int)
	args = parser.parse_args()
	if args.alg == "BnB":
		BnB(args.inst,args.time)
	if args.alg == "Approx":
		Approx(args.inst,args.time,args.seed)
	if args.alg == "SA":
		SA(args.inst,args.time,args.seed)
	if args.alg == "HC":
		HCOnce(args.inst,args.time,args.seed)