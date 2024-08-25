# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
import os
import scipy.special as sp
import src.view.Frequency_1 as Frequency_1
import src.view.BlockFrequency_2 as BlockFrequency_2
import src.view.Runs_3 as Runs_3
import src.view.LongestRunOfOnes_4 as LongestRunOfOnes_4
import src.view.Rank_5 as Rank_5
import src.view.DiscreteFourierTransform_6 as DiscreteFourierTransform_6
import src.view.NonOverlappingTemplateMatchings_7 as NonOverlappingTemplateMatchings_7
import src.view.OverlappingTemplateMatchings_8 as OverlappingTemplateMatchings_8
import src.view.Universal_9 as Universal_9
import src.view.LinearComplexity_10 as LinearComplexity_10
import src.view.SerialTest_11 as SerialTest_11
import src.view.ApproximateEntropy_12 as ApproximateEntropy_12
import src.view.CumulativeSums_13 as CumulativeSums_13
import src.view.RandomExcursions_14 as RandomExcursions_14
import src.view.RandomExcursionsVariant_15 as RandomExcurisonsVariant_15
import src.view.PRNG_LCG_1 as PRNG_LCG_1
import src.view.PRNG_QCG_1_2 as PRNG_QCG_1_2
import src.view.PRNG_QCG_2_3 as PRNG_QCG_2_3
import src.view.PRNG_CCG_4 as PRNG_CCG_4
import src.view.PRNG_XORG_5 as PRNG_XORG_5
import src.view.AlgorithmTestingFrame as AlgorithmTestingFrame

class MainWindow(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        # Attributes
        self.panel_derecho_actual = None
        self.title('NIST')
        #MENUFRAME
        self.menuframe = ttk.Frame(self, style='Card.TFrame', padding=(8, 4, 8, 4))
        self.menuframe.grid(row=0, column=0, padx=10, pady=10)
        self.file_dir_name = ttk.Label(self.menuframe, text="Nombre del Archivo:" )
        self.file_dir_name.grid(row=0, column=0, padx=10, pady=5, sticky="we")
        self.file_dir_entry = ttk.Entry(self.menuframe)
        self.file_dir_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")
        self.prng_entry = ttk.Label(self.menuframe, text="Seleccion de Generador")
        self.prng_entry.grid(row=1, column=0, padx=10, pady=5, sticky="we")
        self.options = ["Fichero Entrada", "Congruencial Lineal", "Congruencial Cuadratico I",
                    "Congruencial Cuadratico II", "Congruencial Cubico", "XOR"]
        self.combobox = ttk.Combobox(self.menuframe, values=self.options)
        self.combobox.grid(row=1, column=1, padx=10, pady=5, sticky="we")
        self.combobox.current(0)
        self.length_n_name = ttk.Label(self.menuframe, text="Cantidad de Digitos:")
        self.length_n_name.grid(row=2, column=0, padx=10, pady=5, sticky="we")
        self.length_n_entry = ttk.Entry(self.menuframe)
        self.length_n_entry.grid(row=2, column=1, padx=10, pady=5, sticky="we")
        self.number_of_chains_name = ttk.Label(self.menuframe, text="Cantidad de Cadenas:")
        self.number_of_chains_name.grid(row=3, column=0, padx=10, pady=5, sticky="we")
        self.number_of_chains_entry = ttk.Entry(self.menuframe)
        self.number_of_chains_entry.grid(row=3, column=1, padx=10, pady=5, sticky="we")
        self.tests_to_run_frame = ttk.Labelframe(self.menuframe)
        self.tests_to_run_frame.grid(row=4, column=0, padx=10, pady=10, columnspan=2)
        self.test_value_list = []
        for i in range(15):
            row = i // 5
            col = i % 5
            self.test_value = tk.BooleanVar()
            self.test_value_list.append(self.test_value)
            self.chk = ttk.Checkbutton(self.tests_to_run_frame, text=f"Test {i+1}", variable=self.test_value_list[i])
            self.chk.grid(row=row, column=col, padx=5, pady=5, sticky="w")
        self.all_var = tk.BooleanVar()
        self.execute_all = ttk.Checkbutton(self.tests_to_run_frame, text="Ejecutar Todos",
                                           variable=self.all_var, command=self.select_all)
        self.execute_all.grid(row=4, column=0, padx=5, pady=5, columnspan=5, sticky="w")
        self.execute_all.state(['!alternate'])
        self.execute_all.state(['!selected'])
        self.execute_button = ttk.Button(self.menuframe, text="Ejecutar")
        self.execute_button.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.execute_button.bind("<Button-1>", lambda event: self.execute_test())

        self.app_dir = self.app_location()
        print(self.app_dir)
        self.button_frame = ttk.Frame(self, style='Card.TFrame', padding=(8, 4, 8, 4))
        self.button_frame.grid(row=0, column=1, padx=10, pady=10)
        self.AlgorithmTesting_button = ttk.Button(self.button_frame, text="Test Fichero")
        self.AlgorithmTesting_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.AlgorithmTesting_button.bind("<Button-1>", lambda event: self.algorithmtestingframe(str(self.app_dir) + "/experiments/AlgorithmTesting"))
        self.LCG_button = ttk.Button(self.button_frame, text="LCG")
        self.LCG_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.LCG_button.bind("<Button-1>", lambda event: self.algorithmtestingframe(str(self.app_dir) + "/experiments/LCG"))
        self.QCG_1_button = ttk.Button(self.button_frame, text="QCG_1")
        self.QCG_1_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.QCG_1_button.bind("<Button-1>", lambda event: self.algorithmtestingframe(str(self.app_dir) + "/experiments/QCG_1"))
        self.QCG_2_button = ttk.Button(self.button_frame, text="QCG_2")
        self.QCG_2_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.QCG_2_button.bind("<Button-1>", lambda event: self.algorithmtestingframe(str(self.app_dir) + "/experiments/QCG_2"))
        self.CCG_button = ttk.Button(self.button_frame, text="CCG")
        self.CCG_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.CCG_button.bind("<Button-1>", lambda event: self.algorithmtestingframe(str(self.app_dir) + "/experiments/CCG"))
        self.XORG_button = ttk.Button(self.button_frame, text="XORG")
        self.XORG_button.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        self.XORG_button.bind("<Button-1>", lambda event: self.algorithmtestingframe(str(self.app_dir) + "/experiments/XORG"))

        self.create_number()

    def select_all(self):
        # Cambia el estado de todos los checkbuttons según el estado del checkbutton "Ejecutar Todos"
        state = self.all_var.get()
        for var in self.test_value_list:
            var.set(state)

    def execute_test(self):
        self.end_ex_label = ttk.Label(self.menuframe, text="Ejecutando", foreground="black")
        self.end_ex_label.grid(row=5, column=1, padx=10, pady=10, sticky="w")
        self.chains = []
        self.resultado = ["NO EJECUTADO"]*15
        self.data = self.file_dir_entry.get()
        self.n = int(self.length_n_entry.get())
        self.number_of_chains = int(self.number_of_chains_entry.get())
        # Metodo que busca la ruta de la APP
        self.app_dir = self.app_location()
        self.generator = self.combobox.get()
        if self.generator == self.options[0]:
            self.chain_location = str(self.app_dir) + '/data/' + str(self.data)
            self.chains = self.file_to_list(self.chain_location, self.n, self.number_of_chains)
            self.dir_location = str(self.app_dir) + "/experiments/AlgorithmTesting"
        elif self.generator == self.options[1]:
            #(semilla = 03962406)
            self.chains = PRNG_LCG_1.PRNG_LCG(23482349, 1103515245, self.n, self.number_of_chains)
            self.dir_location = str(self.app_dir) + "/experiments/LCG"
        elif self.generator == self.options[2]:
            seed_hex = "7844506a9456c564b8b8538e0cc15aff46c95e69600f084f0657c2401b3c244734b62ea9bb95be4923b9b7e84eeaf1a224894ef0328d44bc3eb3e983644da3f5"
            p = "987b6a6bf2c56a97291c445409920032499f9ee7ad128301b5d0254aa1a9633fdbd378d40149f1e23a13849f3d45992f5c4c6b7104099bc301f6005f9d8115e1"
            self.chains = PRNG_QCG_1_2.transform_to_format(p, seed_hex, self.n, self.number_of_chains)
            self.dir_location = str(self.app_dir) + "/experiments/QCG_1"
        elif self.generator == self.options[3]:
            seed_hex = "7844506a9456c564b8b8538e0cc15aff46c95e69600f084f0657c2401b3c244734b62ea9bb95be4923b9b7e84eeaf1a224894ef0328d44bc3eb3e983644da3f5"
            self.chains = PRNG_QCG_2_3.transform_to_format(seed_hex, self.n, self.number_of_chains)
            self.dir_location = str(self.app_dir) + "/experiments/QCG_2"
        elif self.generator == self.options[4]:
            seed_hex = "7844506a9456c564b8b8538e0cc15aff46c95e69600f084f0657c2401b3c244734b62ea9bb95be4923b9b7e84eeaf1a224894ef0328d44bc3eb3e983644da3f5"
            self.chains = PRNG_CCG_4.transform_to_format(seed_hex, self.n, self.number_of_chains)
            self.dir_location = str(self.app_dir) + "/experiments/CCG"
        elif self.generator == self.options[5]:
            seed = "0001011011011001000101111001001010011011101101000100000010101111111010100100001010110110000000000100110000101110011111111100111"
            self.chains = PRNG_XORG_5.transform_to_format(seed, self.n, self.number_of_chains)
            self.dir_location = str(self.app_dir) + "/experiments/XORG"

        # Vemos que test están seleccionados, la lista contiene numeros de 1 a 15 indicandonos
        # esos numeros que test son los que se quieren ejecutar
        self.selected_tests = [i + 1 for i, var in enumerate(self.test_value_list) if var.get()]
        self.count_0_s_and_1_s(self.chains)
        self.count = 100

        with open(self.dir_location + "/finalAnalysisReport.txt", "w") as summary_file:
            summary_file.write("------------------------------------------------------------------------------\n")
            summary_file.write("RESULTS FOR THE UNIFORMITY OF P-VALUES AND THE PROPORTION OF PASSING SEQUENCES\n")
            summary_file.write("------------------------------------------------------------------------------\n")
            if self.generator == self.options[0]:
                summary_file.write(f"generator is data/{str(self.data)}\n")
            else:
                summary_file.write(f"generator is {self.generator}\n")
            summary_file.write("------------------------------------------------------------------------------\n")
            summary_file.write(" C1  C2  C3  C4  C5  C6  C7  C8  C9 C10  P-VALUE  PROPORTION  STATISTICAL TEST\n")
            summary_file.write("------------------------------------------------------------------------------\n")
        summary_file.close()

        if 1 in self.selected_tests:
            with open(self.dir_location + "/Frequency/stats.txt", "w") as stats_file:
                pass
            with open(self.dir_location + "/Frequency/results.txt", "w") as results_file:
                pass
            for i in range(self.number_of_chains):
                self.resultado[0] = Frequency_1.Frequency(self.n, self.chains[i], self.dir_location)
            with open(self.dir_location + "/Frequency/results.txt", "r") as results_file:
                C = [0]*10
                count = 0
                for line in results_file:
                    p_value = float(line.strip())
                    if p_value >= 0.01:
                        count = count + 1
                    category = int((p_value * 10) % 10)
                    C[category] = C[category] + 1
            results_file.close()
            with open(self.dir_location + "/finalAnalysisReport.txt", "a") as summary_file:
                for i in range(10):
                    formatted_number = f"{C[i]:3}"
                    summary_file.write(formatted_number + ' ')
                chi_2 = 0.0
                for i in range(10):
                    chi_2 = chi_2 + ((C[i] - sum(C)/10)**2) / (sum(C)/10)
                p_value = sp.gammaincc(9/2 , chi_2/2)
                if sum(C) < 10:
                    summary_file.write(f" --------")
                else:
                    summary_file.write(f" {p_value:.6f}")
                summary_file.write(f" {count:5}/{sum(C)}     ")
                summary_file.write("Frequency\n")
            summary_file.close()

        if 2 in self.selected_tests:
            with open(self.dir_location + "/BlockFrequency/stats.txt", "w") as stats_file:
                pass
            with open(self.dir_location + "/BlockFrequency/results.txt", "w") as results_file:
                pass
            for i in range(self.number_of_chains):
                self.resultado[1] = BlockFrequency_2.BlockFrequency(self.n, 128, self.chains[i], self.dir_location)
            with open(self.dir_location + "/BlockFrequency/results.txt", "r") as results_file:
                C = [0]*10
                count = 0
                for line in results_file:
                    p_value = float(line.strip())
                    if p_value >= 0.01:
                        count = count + 1
                    category = int((p_value * 10) % 10)
                    C[category] = C[category] + 1
            results_file.close()
            with open(self.dir_location + "/finalAnalysisReport.txt", "a") as summary_file:
                for i in range(10):
                    formatted_number = f"{C[i]:3}"
                    summary_file.write(formatted_number + ' ')
                chi_2 = 0.0
                for i in range(10):
                    chi_2 = chi_2 + ((C[i] - sum(C)/10)**2) / (sum(C)/10)
                p_value = sp.gammaincc(9/2 , chi_2/2)
                if sum(C) < 10:
                    summary_file.write(f" --------")
                else:
                    summary_file.write(f" {p_value:.6f}")
                summary_file.write(f" {count:5}/{sum(C)}     ")
                summary_file.write("BlockFrequency\n")
            summary_file.close()

        if 3 in self.selected_tests:
            with open(self.dir_location + "/Runs/stats.txt", "w") as stats_file:
                pass
            with open(self.dir_location + "/Runs/results.txt", "w") as results_file:
                pass
            for i in range(self.number_of_chains):
                self.resultado[2] = Runs_3.Runs(self.n, self.chains[i], self.dir_location)
            with open(self.dir_location + "/Runs/results.txt", "r") as results_file:
                C = [0]*10
                count = 0
                for line in results_file:
                    p_value = float(line.strip())
                    if p_value >= 0.01:
                        count = count + 1
                    category = int((p_value * 10) % 10)
                    C[category] = C[category] + 1
            results_file.close()
            with open(self.dir_location + "/finalAnalysisReport.txt", "a") as summary_file:
                for i in range(10):
                    formatted_number = f"{C[i]:3}"
                    summary_file.write(formatted_number + ' ')
                chi_2 = 0.0
                for i in range(10):
                    chi_2 = chi_2 + ((C[i] - sum(C)/10)**2) / (sum(C)/10)
                p_value = sp.gammaincc(9/2 , chi_2/2)
                if sum(C) < 10:
                    summary_file.write(f" --------")
                else:
                    summary_file.write(f" {p_value:.6f}")
                summary_file.write(f" {count:5}/{sum(C)}     ")
                summary_file.write("Runs\n")
            summary_file.close()

        if 4 in self.selected_tests:
            with open(self.dir_location + "/LongestRunOfOnes/stats.txt", "w") as stats_file:
                pass
            with open(self.dir_location + "/LongestRunOfOnes/results.txt", "w") as results_file:
                pass
            for i in range(self.number_of_chains):
                self.resultado[3] = LongestRunOfOnes_4.LongestRunOfOnes(self.n, self.chains[i], self.dir_location)
            with open(self.dir_location + "/LongestRunOfOnes/results.txt", "r") as results_file:
                C = [0]*10
                count = 0
                for line in results_file:
                    p_value = float(line.strip())
                    if p_value >= 0.01:
                        count = count + 1
                    category = int((p_value * 10) % 10)
                    C[category] = C[category] + 1
            results_file.close()
            with open(self.dir_location + "/finalAnalysisReport.txt", "a") as summary_file:
                for i in range(10):
                    formatted_number = f"{C[i]:3}"
                    summary_file.write(formatted_number + ' ')
                chi_2 = 0.0
                for i in range(10):
                    chi_2 = chi_2 + ((C[i] - sum(C)/10)**2) / (sum(C)/10)
                p_value = sp.gammaincc(9/2 , chi_2/2)
                if sum(C) < 10:
                    summary_file.write(f" --------")
                else:
                    summary_file.write(f" {p_value:.6f}")
                summary_file.write(f" {count:5}/{sum(C)}     ")
                summary_file.write("LongestRunOfOnes\n")
            summary_file.close()

        if 5 in self.selected_tests:
            with open(self.dir_location + "/Rank/stats.txt", "w") as stats_file:
                pass
            with open(self.dir_location + "/Rank/results.txt", "w") as results_file:
                pass
            for i in range(self.number_of_chains):
                self.resultado[4] = Rank_5.Rank(self.n, self.chains[i], self.dir_location)
            with open(self.dir_location + "/Rank/results.txt", "r") as results_file:
                C = [0]*10
                count = 0
                for line in results_file:
                    p_value = float(line.strip())
                    if p_value >= 0.01:
                        count = count + 1
                    category = int((p_value * 10) % 10)
                    C[category] = C[category] + 1
            results_file.close()
            with open(self.dir_location + "/finalAnalysisReport.txt", "a") as summary_file:
                for i in range(10):
                    formatted_number = f"{C[i]:3}"
                    summary_file.write(formatted_number + ' ')
                chi_2 = 0.0
                for i in range(10):
                    chi_2 = chi_2 + ((C[i] - sum(C)/10)**2) / (sum(C)/10)
                p_value = sp.gammaincc(9/2 , chi_2/2)
                if sum(C) < 10:
                    summary_file.write(f" --------")
                else:
                    summary_file.write(f" {p_value:.6f}")
                summary_file.write(f" {count:5}/{sum(C)}     ")
                summary_file.write("Rank\n")
            summary_file.close()
            print("ACABO EL 5")

        if 6 in self.selected_tests:
            with open(self.dir_location + "/DiscreteFourierTransform/stats.txt", "w") as stats_file:
                pass
            with open(self.dir_location + "/DiscreteFourierTransform/results.txt", "w") as results_file:
                pass
            for i in range(self.number_of_chains):
                self.resultado[5] = DiscreteFourierTransform_6.DiscreteFourierTransform(self.n, self.chains[i], self.dir_location)
            with open(self.dir_location + "/DiscreteFourierTransform/results.txt", "r") as results_file:
                C = [0]*10
                count = 0
                for line in results_file:
                    p_value = float(line.strip())
                    if p_value >= 0.01:
                        count = count + 1
                    category = int((p_value * 10) % 10)
                    C[category] = C[category] + 1
            results_file.close()
            with open(self.dir_location + "/finalAnalysisReport.txt", "a") as summary_file:
                for i in range(10):
                    formatted_number = f"{C[i]:3}"
                    summary_file.write(formatted_number + ' ')
                chi_2 = 0.0
                for i in range(10):
                    chi_2 = chi_2 + ((C[i] - sum(C)/10)**2) / (sum(C)/10)
                p_value = sp.gammaincc(9/2 , chi_2/2)
                if sum(C) < 10:
                    summary_file.write(f" --------")
                else:
                    summary_file.write(f" {p_value:.6f}")
                summary_file.write(f" {count:5}/{sum(C)}     ")
                summary_file.write("DiscreteFourierTransform\n")
            summary_file.close()
            print("ACABO EL 6")

        if 7 in self.selected_tests:
            with open(self.dir_location + "/NonOverlappingTemplateMatchings/stats.txt", "w") as stats_file:
                pass
            with open(self.dir_location + "/NonOverlappingTemplateMatchings/results.txt", "w") as results_file:
                pass
            for i in range(self.number_of_chains):
                self.resultado[6] = NonOverlappingTemplateMatchings_7.NonOverlappingTemplateMatchings(self.n, 9, self.chains[i], self.dir_location)
            with open(self.dir_location + "/NonOverlappingTemplateMatchings/results.txt", "r") as results_file:
                lines = results_file.readlines()
                lines = [line.strip() for line in lines]
                times = int(len(lines)/self.number_of_chains)
                for i in range(times):
                    C = [0]*10
                    count = 0
                    for j in range(len(lines)):
                        if j % times == (i)%times:
                            p_value = float(lines[j].strip())
                            if p_value >= 0.01:
                                count = count + 1
                            category = int((p_value * 10) % 10)
                            C[category] = C[category] + 1
                    with open(self.dir_location + "/finalAnalysisReport.txt", "a") as summary_file:
                        for i in range(10):
                            formatted_number = f"{C[i]:3}"
                            summary_file.write(formatted_number + ' ')
                        chi_2 = 0.0
                        for i in range(10):
                            chi_2 = chi_2 + ((C[i] - sum(C)/10)**2) / (sum(C)/10)
                        p_value = sp.gammaincc(9/2 , chi_2/2)
                        if sum(C) < 10:
                            summary_file.write(f" --------")
                        else:
                            summary_file.write(f" {p_value:.6f}")
                        summary_file.write(f" {count:5}/{sum(C)}     ")
                        summary_file.write("NonOverlappingTemplateMatchings\n")
            summary_file.close()
            results_file.close()
            print("ACABO EL 7")

        if 8 in self.selected_tests:
            with open(self.dir_location + "/OverlappingTemplateMatchings/stats.txt", "w") as stats_file:
                pass
            with open(self.dir_location + "/OverlappingTemplateMatchings/results.txt", "w") as results_file:
                pass
            for i in range(self.number_of_chains):
                self.resultado[7] = OverlappingTemplateMatchings_8.OverlappingTemplateMatchings(self.n, 9, self.chains[i], self.dir_location)
            with open(self.dir_location + "/OverlappingTemplateMatchings/results.txt", "r") as results_file:
                C = [0]*10
                count = 0
                for line in results_file:
                    p_value = float(line.strip())
                    if p_value >= 0.01:
                        count = count + 1
                    category = int((p_value * 10) % 10)
                    C[category] = C[category] + 1
            results_file.close()
            with open(self.dir_location + "/finalAnalysisReport.txt", "a") as summary_file:
                for i in range(10):
                    formatted_number = f"{C[i]:3}"
                    summary_file.write(formatted_number + ' ')
                chi_2 = 0.0
                for i in range(10):
                    chi_2 = chi_2 + ((C[i] - sum(C)/10)**2) / (sum(C)/10)
                p_value = sp.gammaincc(9/2 , chi_2/2)
                if sum(C) < 10:
                    summary_file.write(f" --------")
                else:
                    summary_file.write(f" {p_value:.6f}")
                summary_file.write(f" {count:5}/{sum(C)}     ")
                summary_file.write("OverlappingTemplateMatchings\n")
            summary_file.close()
            print("ACABO EL 8")

        if 9 in self.selected_tests:
            with open(self.dir_location + "/Universal/stats.txt", "w") as stats_file:
                pass
            with open(self.dir_location + "/Universal/results.txt", "w") as results_file:
                pass
            for i in range(self.number_of_chains):
                self.resultado[8] = Universal_9.Universal(self.n, 5, 1280, self.chains[i], self.dir_location)
            with open(self.dir_location + "/Universal/results.txt", "r") as results_file:
                C = [0]*10
                count = 0
                for line in results_file:
                    p_value = float(line.strip())
                    if p_value >= 0.01:
                        count = count + 1
                    category = int((p_value * 10) % 10)
                    C[category] = C[category] + 1
            results_file.close()
            with open(self.dir_location + "/finalAnalysisReport.txt", "a") as summary_file:
                for i in range(10):
                    formatted_number = f"{C[i]:3}"
                    summary_file.write(formatted_number + ' ')
                if sum(C) == 0:
                    C[9] = self.number_of_chains
                    p_value = 0.000000
                    if sum(C) < 10:
                        summary_file.write(f" --------")
                    else:
                        summary_file.write(f" {p_value:.6f}*")
                else:
                    chi_2 = 0.0
                    for i in range(10):
                        chi_2 = chi_2 + ((C[i] - sum(C)/10)**2) / (sum(C)/10)
                    p_value = sp.gammaincc(9/2 , chi_2/2)
                    if sum(C) < 10:
                        summary_file.write(f" --------")
                    else:
                        summary_file.write(f" {p_value:.6f} ")
                summary_file.write(f" {count:5}/{sum(C)}     ")
                summary_file.write("Universal\n")
            summary_file.close()
            print("ACABO EL 9")

        if 10 in self.selected_tests:
            with open(self.dir_location + "/LinearComplexity/stats.txt", "w") as stats_file:
                pass
            with open(self.dir_location + "/LinearComplexity/results.txt", "w") as results_file:
                pass
            for i in range(self.number_of_chains):
                self.resultado[9] = LinearComplexity_10.LinearComplexity(self.n, 500, self.chains[i], self.dir_location)
            with open(self.dir_location + "/LinearComplexity/results.txt", "r") as results_file:
                C = [0]*10
                count = 0
                for line in results_file:
                    p_value = float(line.strip())
                    if p_value >= 0.01:
                        count = count + 1
                    category = int((p_value * 10) % 10)
                    C[category] = C[category] + 1
            results_file.close()
            with open(self.dir_location + "/finalAnalysisReport.txt", "a") as summary_file:
                for i in range(10):
                    formatted_number = f"{C[i]:3}"
                    summary_file.write(formatted_number + ' ')
                chi_2 = 0.0
                for i in range(10):
                    chi_2 = chi_2 + ((C[i] - sum(C)/10)**2) / (sum(C)/10)
                p_value = sp.gammaincc(9/2 , chi_2/2)
                if sum(C) < 10:
                    summary_file.write(f" --------")
                else:
                    summary_file.write(f" {p_value:.6f}")
                summary_file.write(f" {count:5}/{sum(C)}     ")
                summary_file.write("LinearComplexity\n")
            summary_file.close()
            print("ACABO EL 10")

        if 11 in self.selected_tests:
            with open(self.dir_location + "/SerialTest/stats.txt", "w") as stats_file:
                pass
            with open(self.dir_location + "/SerialTest/results.txt", "w") as results_file:
                pass
            for i in range(self.number_of_chains):
                self.resultado[10] = SerialTest_11.SerialTest(self.n, 16, self.chains[i], self.dir_location)
            with open(self.dir_location + "/SerialTest/results.txt", "r") as results_file:
                lines = results_file.readlines()
                lines = [line.strip() for line in lines]
                for i in range(2):
                    C = [0]*10
                    count = 0
                    for j in range(len(lines)):
                        if j % 2 == (i)%2:
                            p_value = float(lines[j].strip())
                            if p_value >= 0.01:
                                count = count + 1
                            category = int((p_value * 10) % 10)
                            C[category] = C[category] + 1
                    with open(self.dir_location + "/finalAnalysisReport.txt", "a") as summary_file:
                        for i in range(10):
                            formatted_number = f"{C[i]:3}"
                            summary_file.write(formatted_number + ' ')
                        chi_2 = 0.0
                        for i in range(10):
                            chi_2 = chi_2 + ((C[i] - sum(C)/10)**2) / (sum(C)/10)
                        p_value = sp.gammaincc(9/2 , chi_2/2)
                        if sum(C) < 10:
                            summary_file.write(f" --------")
                        else:
                            summary_file.write(f" {p_value:.6f}")
                        summary_file.write(f" {count:5}/{sum(C)}     ")
                        summary_file.write("SerialTest\n")
            summary_file.close()
            results_file.close()
            print("ACABO EL 11")

        if 12 in self.selected_tests:
            with open(self.dir_location + "/ApproximateEntropy/stats.txt", "w") as stats_file:
                pass
            with open(self.dir_location + "/ApproximateEntropy/results.txt", "w") as results_file:
                pass
            for i in range(self.number_of_chains):
                self.resultado[11] = ApproximateEntropy_12.ApproximateEntropy(self.n, 10, self.chains[i], self.dir_location)
            with open(self.dir_location + "/ApproximateEntropy/results.txt", "r") as results_file:
                C = [0]*10
                count = 0
                for line in results_file:
                    p_value = float(line.strip())
                    if p_value >= 0.01:
                        count = count + 1
                    category = int((p_value * 10) % 10)
                    C[category] = C[category] + 1
            results_file.close()
            with open(self.dir_location + "/finalAnalysisReport.txt", "a") as summary_file:
                for i in range(10):
                    formatted_number = f"{C[i]:3}"
                    summary_file.write(formatted_number + ' ')
                chi_2 = 0.0
                for i in range(10):
                    chi_2 = chi_2 + ((C[i] - sum(C)/10)**2) / (sum(C)/10)
                p_value = sp.gammaincc(9/2 , chi_2/2)
                if sum(C) < 10:
                    summary_file.write(f" --------")
                else:
                    summary_file.write(f" {p_value:.6f}")
                summary_file.write(f" {count:5}/{sum(C)}     ")
                summary_file.write("ApproximateEntropy\n")
            summary_file.close()
            print("ACABO EL 12")

        if 13 in self.selected_tests:
            with open(self.dir_location + "/CumulativeSums/stats.txt", "w") as stats_file:
                pass
            with open(self.dir_location + "/CumulativeSums/results.txt", "w") as results_file:
                pass
            for i in range(self.number_of_chains):
                self.resultado[12] = CumulativeSums_13.CumulativeSums(self.n, self.chains[i], self.dir_location)
            with open(self.dir_location + "/CumulativeSums/results.txt", "r") as results_file:
                lines = results_file.readlines()
                lines = [line.strip() for line in lines]
                for i in range(2):
                    C = [0]*10
                    count = 0
                    for j in range(len(lines)):
                        if j % 2 == (i)%2:
                            p_value = float(lines[j].strip())
                            if p_value >= 0.01:
                                count = count + 1
                            category = int((p_value * 10) % 10)
                            C[category] = C[category] + 1
                    with open(self.dir_location + "/finalAnalysisReport.txt", "a") as summary_file:
                        for i in range(10):
                            formatted_number = f"{C[i]:3}"
                            summary_file.write(formatted_number + ' ')
                        chi_2 = 0.0
                        for i in range(10):
                            chi_2 = chi_2 + ((C[i] - sum(C)/10)**2) / (sum(C)/10)
                        p_value = sp.gammaincc(9/2 , chi_2/2)
                        if sum(C) < 10:
                            summary_file.write(f" --------")
                        else:
                            summary_file.write(f" {p_value:.6f}")
                        summary_file.write(f" {count:5}/{sum(C)}     ")
                        summary_file.write("CumulativeSums\n")
            summary_file.close()
            results_file.close()
            print("ACABO EL 13")

        if 14 in self.selected_tests:
            with open(self.dir_location + "/RandomExcursions/stats.txt", "w") as stats_file:
                pass
            with open(self.dir_location + "/RandomExcursions/results.txt", "w") as results_file:
                pass
            for i in range(self.number_of_chains):
                self.resultado[13] = RandomExcursions_14.RandomExcursions(self.n, self.chains[i], self.dir_location)
            aux = 1.0
            with open(self.dir_location + "/RandomExcursions/results.txt", "r") as results_file:
                lines = results_file.readlines()
                lines = [line.strip() for line in lines]
                for i in range(8):
                    C = [0]*10
                    count = 0
                    for j in range(len(lines)):
                        if j % 8 == (i)%8:
                            p_value = float(lines[j].strip())
                            if p_value >= 0.01:
                                count = count + 1
                            if p_value == 0.0:
                                aux = 0.0
                            else:
                                category = int((p_value * 10) % 10)
                                C[category] = C[category] + 1
                    with open(self.dir_location + "/finalAnalysisReport.txt", "a") as summary_file:
                        for i in range(10):
                            formatted_number = f"{C[i]:3}"
                            summary_file.write(formatted_number + ' ')
                        if sum(C) == 0.0:
                            summary_file.write(" --------")
                            summary_file.write("  ---------  ")
                        elif aux == 0.0 or sum(C) < 10:
                            summary_file.write(" --------")
                            summary_file.write(f" {count:5}/{sum(C)}     ")
                        else:
                            chi_2 = 0.0
                            for i in range(10):
                                chi_2 = chi_2 + ((C[i] - sum(C)/10)**2) / (sum(C)/10)
                            p_value = sp.gammaincc(9/2 , chi_2/2)
                            summary_file.write(f" {p_value:.6f}")
                            summary_file.write(f" {count:5}/{sum(C)}     ")
                        summary_file.write("RandomExcursions\n")
            summary_file.close()
            results_file.close()
            self.count = sum(C)
            print("ACABO EL 14")

        if 15 in self.selected_tests:
            with open(self.dir_location + "/RandomExcursionsVariant/stats.txt", "w") as stats_file:
                pass
            with open(self.dir_location + "/RandomExcursionsVariant/results.txt", "w") as results_file:
                pass
            for i in range(self.number_of_chains):
                self.resultado[14] = RandomExcurisonsVariant_15.RandomExcursionsVariant(self.n, self.chains[i], self.dir_location)
            aux = 1.0
            with open(self.dir_location + "/RandomExcursionsVariant/results.txt", "r") as results_file:
                lines = results_file.readlines()
                lines = [line.strip() for line in lines]
                for i in range(18):
                    C = [0]*10
                    self.count = 0
                    for j in range(len(lines)):
                        if j % 18 == (i)%18:
                            p_value = float(lines[j].strip())
                            if p_value >= 0.01:
                                self.count = self.count + 1
                            if p_value == 0.0:
                                aux = 0.0
                            else:
                                category = int((p_value * 10) % 10)
                                C[category] = C[category] + 1
                    with open(self.dir_location + "/finalAnalysisReport.txt", "a") as summary_file:
                        for i in range(10):
                            formatted_number = f"{C[i]:3}"
                            summary_file.write(formatted_number + ' ')
                        if sum(C) == 0.0:
                            summary_file.write(" --------")
                            summary_file.write("  ---------  ")
                        elif aux == 0.0 or sum(C) < 10:
                            summary_file.write(" --------")
                            summary_file.write(f" {self.count:5}/{sum(C)}     ")
                        else:
                            chi_2 = 0.0
                            for i in range(10):
                                chi_2 = chi_2 + ((C[i] - sum(C)/10)**2) / (sum(C)/10)
                            p_value = sp.gammaincc(9/2 , chi_2/2)
                            summary_file.write(f" {p_value:.6f}")
                            summary_file.write(f" {self.count:5}/{sum(C)}     ")
                        summary_file.write("RandomExcursionsVariant\n")
                        self.count = sum(C)
            summary_file.close()
            results_file.close()
        with open(self.dir_location + "/finalAnalysisReport.txt", "a") as summary_file:
            summary_file.write("------------------------------------------------------------------------------\n")
            summary_file.write("La tasa minima de aceptacion para cada test estadistico con excepcion\n")
            self.minimun_pass = int((0.99-3*((0.99*0.01/self.number_of_chains)**(1/2)))*self.number_of_chains)
            summary_file.write(f"del test Random Excurison y su Variante es de aproximadamente una proporcion\n")
            summary_file.write(f"de {self.minimun_pass}/{self.number_of_chains} secuencias binarias.\n\n")
            if self.count == 100:
                pass
            else:
                summary_file.write(f"La tasa minima de aceptacion para el test Random Excursion y su Variante\n")
                self.minimun_pass = int((0.99-3*((0.99*0.01/self.count)**(1/2)))*self.count)
                summary_file.write(f"es de aproximadamente una proporcion de {self.minimun_pass}/{self.count} secuencias binarias.\n")
            summary_file.write("------------------------------------------------------------------------------\n")
        summary_file.close()
        self.end_ex_label = ttk.Label(self.menuframe, text="Fin de la Ejecucion.", foreground="black")
        self.end_ex_label.grid(row=5, column=1, padx=10, pady=10, sticky="w")



    def app_location(self):
        # Ruta absoluta del archivo MainWindow.py porque es el que se está ejecutando cuando se llama al metodo
        ruta_script = os.path.abspath(__file__)
        # Directorio que contiene el archivo del script
        directorio_script = os.path.dirname(ruta_script)
        # Borramos dos directorios hasta llegar a la carpeta APP_TFG
        directorio_app = os.path.dirname(os.path.dirname(directorio_script))
        directorio_app = directorio_app.replace("\\", "/")
        return directorio_app

    def file_to_list(self, filepath, length, number_of_chains):
        # Inicializar una lista vacía para almacenar los números
        result = []
        chain = []
        try:
            # Abrir y leer el archivo
            with open(filepath, 'r') as file:
                # Leer el contenido del archivo y eliminar espacios y saltos de línea
                content = file.read().replace('\n', '').replace(' ', '')

                # Iterar sobre cada carácter en el contenido limpio
                for char in content:
                    # Comprobar si el carácter es '0' o '1'
                    if char in '01':
                        # Convertir el carácter a entero y añadir a la lista
                        chain.append(int(char))
                        if length is not None and len(chain) >= length:
                            result.append(chain)
                            chain = []
                            if len(result) == number_of_chains:
                                break

        except FileNotFoundError:
            print(f"El archivo {filepath} no se encontró.")
        except IOError:
            print(f"Error al leer el archivo {filepath}.")

        return result

    def count_0_s_and_1_s(self, chains):
        with open(self.dir_location + "/freq.txt", "w") as freq_file:
            freq_file.write("______________________________________________________\n\n")
            if self.generator == self.options[0]:
                freq_file.write(f"generator is data/{str(self.data)}\n")
            else:
                freq_file.write(f"generator is {self.generator}\n")
            freq_file.write("______________________________________________________\n\n")
        for chain in chains:
            number_of_1s = 0
            for bit in chain:
                if bit == 1:
                    number_of_1s = number_of_1s + 1
            number_of_0s = self.n - number_of_1s
            with open(self.dir_location + "/freq.txt", "a") as freq_file:
                freq_file.write(f"\tBITSREAD = {self.n}  0s = {number_of_0s}  1s = {number_of_1s}\n")

    def algorithmtestingframe(self, dir_location):
        title = dir_location
        algorithm = AlgorithmTestingFrame.AlgorithmTestingFrame(self, title, dir_location)

    def create_number(self):
        list_of_list_LCG = PRNG_LCG_1.PRNG_LCG(3962406, 1103515245, 127, 1)
        list_LCG = list_of_list_LCG[0]
        XORG_seed = ''.join(str(bit) for bit in list_LCG)
        list_of_list_XORG = PRNG_XORG_5.transform_to_format(XORG_seed, 10000000, 1)
        lista_XORG = list_of_list_XORG[0]
        number_generated = ''.join(str(bit) for bit in lista_XORG)
        with open(str(self.app_dir) + "/data/my_number_generated.txt", 'w') as file:
            file.write(number_generated)