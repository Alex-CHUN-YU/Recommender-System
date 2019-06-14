# -*- coding: utf-8 -*-
__author__ = "ALEX-CHUN-YU (P76064538@mail.ncku.edu.tw)"
from sum_w2v_w2v_sg import Sum_W2V_W2V_SG
from e2v_w2v_sg import E2V_W2V_SG

# Main Embedding Method
def main():
	# Sum_W2V_W2V_SG(Baseline Vector) 根據需求要去 setting 
	# sum_w2v_w2v_sg = Sum_W2V_W2V_SG()
	# sum_w2v_w2v_sg.sum_w2v_w2v_sg()
	# E2V_W2V_SG 根據需求要去 setting 
	e2v_w2v_sg = E2V_W2V_SG()
	e2v_w2v_sg.e2v_w2v_sg()
if __name__ == "__main__":
	main()