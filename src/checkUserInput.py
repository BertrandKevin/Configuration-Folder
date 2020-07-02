#!/usr/bin/python

import sys

def question_and_verification(question):
	answer = ""

	while answer != "y" and answer != "n":
		try:
			answer = input(question)
			print("Reponse donnee: " + str(answer))
		except:
			print("error")

		if "exit" in answer:
			exit()

		try:
			answer = answer.lower()
		except:
			print("La valeur est eronee!")

	return answer
