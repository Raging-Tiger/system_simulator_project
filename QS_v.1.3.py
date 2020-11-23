import tkinter as tk
from tkinter import ttk
from math import pi, sin, cos
import matplotlib.pyplot as plt
from random import randrange, uniform
import pickle
import os
import sys
from itertools import product
import re

#####
#Functions with:
# CORE - main calculation/etc used by the other functions
# READ - wrappers for CORE or any display from main frame
# MENU - any functions triggered from upper menu
#####

#Core class for frames manipulation
class core_frame(tk.Tk):
    def __init__(self):
        
        tk.Tk.__init__(self)
        
        tk.Tk.iconbitmap(self, default=(os.path.join(sys.path[0], r"fav1.ico")))
        tk.Tk.wm_title(self, "Simulator")
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Initial_choice, Quantum_simulator, Classical_simulator):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Initial_choice)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        menubar = frame.menubar(self)
        self.configure(menu=menubar)
        
        

#First frame of choosing between systems
class Initial_choice(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Select system to simulate")
        label.pack(pady=10,padx=10)
        self.photo = tk.PhotoImage(file = (os.path.join(sys.path[0], r"quant_ico.png"))) 
        self.icon_quant = self.photo.subsample(2, 2)
        button1 = ttk.Button(self, text="Quantum system",
                            command=lambda: controller.show_frame(Quantum_simulator), image = self.icon_quant, compound = tk.BOTTOM)
        button1.place(relx=0.22, rely=0.5, anchor='w')

        #self.photo_class = tk.PhotoImage(file = (os.path.join(sys.path[0], r"class_icon.png"))) 
        self.photo_class = tk.PhotoImage(file = (os.path.join(sys.path[0], r"0101.png"))) 
        self.icon_class = self.photo_class.subsample(2, 2)

        button2 = ttk.Button(self, text="Classical system",
                            command=lambda: controller.show_frame(Classical_simulator), image = self.icon_class, compound = tk.BOTTOM)
        button2.place(in_=button1, anchor="c", relx=2, rely = 0.5)
               
        controller.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(controller))


    def on_closing(self, controller):
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            controller.destroy()

    def menubar(self, parent):
        menubar = tk.Menu(parent)
        return menubar


#Quantum simulator frame
class Quantum_simulator(tk.Frame):

    def __init__(self, parent, controller):

        #Lists for quantum system parameters -- CORE
        self.__quantum_states = []
        self.__basis = [[1,0]]
        self.__basis_theta = [0]

        tk.Frame.__init__(self, parent)
        

        label = tk.Label(self, text="Quantum system functions")
        label.grid(row=0, column=0,columnspan=2, sticky="nsew")
        #Initial function -- create system - Button + entry field
        self.button_new_system = ttk.Button(self, text="Create quantum system", command=self.__create_quantum_system)
        self.quantum_create_system_entry = ttk.Entry(self)
        self.button_new_system.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.quantum_create_system_entry.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        #Text field for log -- Text field, diasabled
        self.text = tk.Text(self, width = 100)
        self.text.grid(row=0, column=7, columnspan=55, rowspan=55, padx=20, pady=20, sticky="e")
        scrollb = ttk.Scrollbar(self, command=self.text.yview)
        scrollb.grid(row=0, column=7, columnspan=55, rowspan=55, padx=20, pady=20, sticky="nse")
        self.text['yscrollcommand'] = scrollb.set

        self.text.insert(tk.END, 'Here will be showed the history of actions taken in the quantum simulation')
        self.text['state'] = tk.DISABLED

        #Read current state -- Button
        self.button_read_current_state = ttk.Button(self, text="Read current quantum state", command=self.read_current_state)

        #Rotate state by -- Button + entry field
        self.button_rotate = ttk.Button(self, text="Rotate by", command=self.rotate_state)
        self.rotate_entry = ttk.Entry(self)

        #Draw current state - Button
        self.button_draw_current_state = ttk.Button(self, text="Draw current state", command=self.draw_state)

        #Draw all states - Button
        self.button_draw_all_states = ttk.Button(self, text="Draw all visited states", command=self.draw_all_states)

        #Reflect and Reflect and draw - Button x2 + entry field
        self.button_reflect = ttk.Button(self, text="Reflect over", command=self.reflect_state)
        self.button_reflect_and_draw = ttk.Button(self, text="Reflect over and draw", command=self.reflect_and_draw)
        self.reflect_entry = ttk.Entry(self)

        #Current probabilities - Button
        self.button_probs = ttk.Button(self, text="Current probability", command=self.probs_state)

        #Measure outcome and measure and plot - Button x2 + entry field
        self.button_measure = ttk.Button(self, text="Make a measurement", command=self.measure_state)
        self.button_measure_plot = ttk.Button(self, text="Plot measurement", command=self.plot_measure_state)
        self.measure_entry = ttk.Entry(self)

        #Change basis - Button + Entry
        self.button_change_basis_wrap = ttk.Button(self, text="Change basis", command=self.change_basis_wrap)
        self.change_basis_entry = ttk.Entry(self)

        #Draw in prev basis - Button
        self.button_draw_state_prev_basis = ttk.Button(self, text="Draw state in previous basis", command=self.draw_state_in_previous_basis)

        #Prob in 2 basis - Button
        self.button_prob_two_basis = ttk.Button(self, text="Probability of basic states in two bases", command=self.prob_in_both_states)

        #take_back_basis_change
        self.button_remove_basis = ttk.Button(self, text="Remove basis", command=self.take_back_basis_change)

        
        
    #This is a menu to save/load mostly
    def menubar(self, parent):
        menubar = tk.Menu(parent)
        pageMenu = tk.Menu(menubar)
        pageMenu.add_command(label="New", command= lambda: (self.new(parent)))
        pageMenu.add_command(label="Save as", command=self.save_as)
        pageMenu.add_command(label="Save history as", command=self.save_history_as)
        pageMenu.add_command(label="Load", command=self.load)
        pageMenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=pageMenu)

        analysisMenu = tk.Menu(menubar)
        analysisMenu.add_command(label="Plot X", command=self.plot_x)
        analysisMenu.add_command(label="Plot Y", command=self.plot_y)
        analysisMenu.add_command(label="Plot X and Y", command=self.plot_x_y)
        analysisMenu.add_command(label="Plot probability of X", command=self.plot_x_probs)
        analysisMenu.add_command(label="Plot probability of Y", command=self.plot_y_probs)
        analysisMenu.add_command(label="Plot probability of X and Y", command=self.plot_x_y_probs)
        analysisMenu.add_command(label="Plot X distribution", command=self.plot_x_distribution)
        analysisMenu.add_command(label="Plot Y distribution", command=self.plot_y_distribution)
        menubar.add_cascade(label="Analysis", menu=analysisMenu)
    
        systemMenu = tk.Menu(menubar)
        systemMenu.add_command(label="Info", command=self.system_info)
        systemMenu.add_command(label="Delete state", command=self.delete_state)
        menubar.add_cascade(label="System", menu=systemMenu)
        return menubar


    #Initial state of quantum system -- CORE + READ
    def __create_quantum_system(self):
        input_data = self.quantum_create_system_entry.get()
        theta = 0

        #validating input: 1) is default, 2) entry, 3) reject
        if input_data == '':
            theta = 0
        elif input_data.isdigit() and int(input_data) >= 0 and int(input_data) <= 360:
            theta = int(input_data)
        else:
            self.text['state'] = tk.NORMAL
            self.text.insert(tk.END, '\nInput data for initial quantum state is incorrect')
            self.text['state'] = tk.DISABLED
            return

        if theta == 0:
            state_zero = [1, 0]
            self.__quantum_states.append(state_zero)
        else:
            radian = (theta * pi) / 180
            quant_state = [cos(radian),sin(radian)]
            self.__quantum_states.append(quant_state)

        self.text['state'] = tk.NORMAL    
        self.text.insert(tk.END, '\nInitial quantum state is: ')
        self.text.insert(tk.END, f'|0> {round(self.__quantum_states[-1][0],5)}; |1> {round(self.__quantum_states[-1][1],5)}')
        self.text['state'] = tk.DISABLED

        self.__change_after_creation()
    
    #Hiding create quantum state button and showing the rest of buttons -- READ
    def __change_after_creation(self):
        #Hiding initial option
        self.button_new_system.grid_forget()
        self.quantum_create_system_entry.grid_forget()

        #Showing new options
        self.button_read_current_state.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.button_rotate.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        self.rotate_entry.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
        self.button_draw_current_state.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
        self.button_draw_all_states.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")
        self.button_reflect.grid(row=5, column=0, padx=5, pady=5, sticky="nsew")
        self.button_reflect_and_draw.grid(row=6, column=0, padx=5, pady=5, sticky="nsew")
        self.reflect_entry.grid(row=5, column=1, rowspan=2, padx=5, pady=5)
        self.button_probs.grid(row=7, column=0, padx=5, pady=5, sticky="nsew")
        self.button_measure.grid(row=8, column=0, padx=5, pady=5, sticky="nsew")
        self.button_measure_plot.grid(row=9, column=0, padx=5, pady=5, sticky="nsew")
        self.measure_entry.grid(row=8, column=1, rowspan=2, padx=5, pady=5)
        self.button_change_basis_wrap.grid(row=10, column=0, padx=5, pady=5, sticky="nsew")
        self.change_basis_entry.grid(row=10, column=1, padx=5, pady=5, sticky="nsew")
        self.button_draw_state_prev_basis.grid(row=11, column=0, padx=5, pady=5, sticky="nsew")
        self.button_draw_state_prev_basis.state(["disabled"])
        self.button_prob_two_basis.grid(row=12, column=0, columnspan = 2, padx=5, pady=5, sticky="nsew")
        self.button_remove_basis.grid(row=13, column=0,padx=5, pady=5, sticky="nsew")
        self.button_remove_basis.state(["disabled"])
        self.button_prob_two_basis.state(["disabled"])

    #Changing buttons is empty file was loaded -- READ
    def __change_load_reverse(self):
        #Hiding initial option
        self.button_new_system.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.quantum_create_system_entry.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        #Showing new options
        self.button_read_current_state.grid_forget()
        self.button_rotate.grid_forget()
        self.rotate_entry.grid_forget()
        self.button_draw_current_state.grid_forget()
        self.button_draw_all_states.grid_forget()
        self.button_reflect.grid_forget()
        self.button_reflect_and_draw.grid_forget()
        self.reflect_entry.grid_forget()
        self.button_probs.grid_forget()
        self.button_measure.grid_forget()
        self.button_measure_plot.grid_forget()
        self.measure_entry.grid_forget()
        self.button_change_basis_wrap.grid_forget()
        self.change_basis_entry.grid_forget()
        self.button_draw_state_prev_basis.grid_forget()
        self.button_draw_state_prev_basis.grid_forget()
        self.button_prob_two_basis.grid_forget()
        self.button_remove_basis.grid_forget()
        self.button_remove_basis.grid_forget()
        self.button_prob_two_basis.grid_forget()


    #Current quantum state -- CORE
    def read_state(self):
        return self.__quantum_states[-1]

    #Display current quantum state -- READ
    def read_current_state(self):

        current_state = self.read_state()
        self.text['state'] = tk.NORMAL    
        self.text.insert(tk.END, '\nCurrent quantum state is: ')
        self.text.insert(tk.END, f'|0> {round(current_state[0],5)}; |1> {round(current_state[1],5)}')
        self.text['state'] = tk.DISABLED

    #Rotation -- CORE
    def rotation(self, theta):
        radian = (theta * pi) / 180
        
        R = [
        [cos(radian), -1*sin(radian)],
        [sin(radian), cos(radian)]
        ]
        
        current_state = self.read_state()
        new_state = self.__linear_evolve(R,current_state)
        self.__quantum_states.append(new_state)
        return new_state
    
    #Linear evolve -- CORE
    def __linear_evolve(self, probabilistic_operator, probabilistic_state, n=1):
        for num in range(n):
            result = []
            for i in range(len(probabilistic_operator)):
                summation = 0
                for j in range(len(probabilistic_operator[0])):
                    summation += probabilistic_operator[i][j]*probabilistic_state[j]
                result.append(summation)
            probabilistic_state = result
        return result
    
    #Rotation -- READ
    def rotate_state(self):
        input_data = self.rotate_entry.get()
        theta = 0

        #Validation
        if input_data.isdigit():
            theta = int(input_data)
        elif input_data.startswith('-') and input_data[1:].isdigit():
            theta = int(input_data)
        else:
            self.text['state'] = tk.NORMAL
            self.text.insert(tk.END, '\nInput data for rotation is incorrect')
            self.text['state'] = tk.DISABLED
            return

        self.rotation(theta)
        self.text['state'] = tk.NORMAL
        self.text.insert(tk.END, f'\nQuantum state was rotated by: {theta} degrees')
        self.text['state'] = tk.DISABLED

    #Drawing any unit-circle -- CORE
    def __draw_unit_circle(self, index = -1, title = '0'):

        fig = plt.figure()
        basis = self.__basis[index]
        #print(basis)
        x_1 = round(basis[0],5)
        y_1 = round(basis[1],5)
        
        if title != '0':
            plt.title(title)
        
        radian = pi/2
        
        R = [
        [cos(radian), -1*sin(radian)],
        [sin(radian), cos(radian)]
        ]
        
        orthogonal_basis = self.__linear_evolve(R,basis)
        
        x_2 = round(orthogonal_basis[0],5)
        y_2 = round(orthogonal_basis[1],5)
        
        plt.arrow(0,0,(x_1*1.4),(y_1*1.4),head_width=0.04,head_length=0.08)
        plt.arrow(0,0,(-1*x_1*1.4),(-1*y_1*1.4))
        plt.arrow(0,0,(-1*x_2*1.4),(-1*y_2*1.4))
        plt.arrow(0,0,(x_2*1.4),(y_2*1.4),head_width=0.04,head_length=0.08)
        
        #resizing
        plt.plot(-1.4,-1.4) 
        plt.plot(1.4,1.4)
        #coordinate center
        plt.plot(0,0,'bo')
        plt.text(0.02,-0.1,'0')
        fig.set_size_inches((7, 7))
        #circle
        plt.gca().add_patch(plt.Circle((0,0),1,color='black',fill=False))
        #coordinates lables
        plt.text(x_1*1.1,y_1*1.1-0.08,'x')
        plt.text(x_2*1.1+0.04, y_2*1.1,'y')

    
    #Draws current quantum state on unit circle -- mostly CORE + READ
    def draw_state(self, title = '0'):
        self.__draw_unit_circle()
        if title != '0':
            plt.title(title)
        current_state = self.read_state()
        #lables shifting
        shift_y = 0.02
        shift_x = 0
        if round(current_state[0],5) < 0:
            shift_x = -0.5
        if round(current_state[1],5) < 0:
            shift_y = -0.02
        plt.arrow(0,0,current_state[0]*0.92,current_state[1]*0.92,head_width=0.04,head_length=0.08, color ='b')

        plt.text(current_state[0]*1.02 + shift_x, current_state[1]*1.02+shift_y,'|current state>')
        plt.show()

    #Draws all quantum states on unit circle -- mostly CORE + READ
    def draw_all_states(self):
        self.__draw_unit_circle()
        all_states = self.__quantum_states
        plt.arrow(0,0,all_states[0][0]*0.92,all_states[0][1]*0.92,head_width=0.04,head_length=0.08, color ='b')
        plt.text(all_states[0][0]*1.02, all_states[0][1]*1.02+0.02,'|initial state>')
        #lables shifting
        if len(all_states) > 1:
            for index in range(1, len(all_states)):
                shift_x = 0
                shift_y = 0.025
                if round(all_states[index][1],5) < 0:
                    shift_y = -0.03
                if round(all_states[index][0],5) < 0:
                    shift_x = -0.03
                if round(all_states[index][1],5) < 0 and round(all_states[index][0],5):
                    shift_x = -0.05
                    shift_y = -0.05
                plt.arrow(0,0,all_states[index][0]*0.92,all_states[index][1]*0.92,head_width=0.04,head_length=0.08, color ='b')
                plt.text(all_states[index][0]*1.02+shift_x, all_states[index][1]*1.02+shift_y,f'|{index}>')
        plt.show()

    #Reflection -- CORE
    def reflection(self, theta):
        radian = (theta * pi) / 180
        
        Ref = [
        [cos(2*radian), sin(2*radian)],
        [sin(2*radian), -1*cos(2*radian)]
        ]
        
        current_state = self.read_state()
        new_state = self.__linear_evolve(Ref,current_state)
        self.__quantum_states.append(new_state)
        return new_state

    #Reflection -- READ
    def reflect_state(self):
        input_data = self.reflect_entry.get()
        theta = 0

        #Validation
        if input_data.isdigit() and int(input_data) >= 0 and int(input_data) <= 360:
            theta = int(input_data)
        else:
            self.text['state'] = tk.NORMAL
            self.text.insert(tk.END, '\nInput data for reflection is incorrect')
            self.text['state'] = tk.DISABLED
            return

        self.reflection(theta)
        self.text['state'] = tk.NORMAL
        self.text.insert(tk.END, f'\nQuantum state was reflected by: {theta} degrees')
        self.text['state'] = tk.DISABLED

    #Reflect and draw -- READ
    def reflect_and_draw(self):

        input_data = self.reflect_entry.get()
        theta = 0

        #Validation
        if input_data.isdigit() and int(input_data) >= 0 and int(input_data) <= 360:
            theta = int(input_data)
        else:
            self.text['state'] = tk.NORMAL
            self.text.insert(tk.END, '\nInput data for reflection is incorrect')
            self.text['state'] = tk.DISABLED
            return

        self.text['state'] = tk.NORMAL
        self.text.insert(tk.END, f'\nQuantum state was reflected by: {theta} degrees')
        self.text['state'] = tk.DISABLED

        radian = (theta * pi)/180
        x_cos = cos(radian)
        y_sin = sin(radian)
        angle = [x_cos, y_sin]
        angle_cont = [-1 * angle[0], -1*angle[1]]

        self.__draw_unit_circle()
        current_state = self.read_state()
        #lables shifting
        shift_y = 0.02
        shift_x = 0
        if round(current_state[0],5) < 0:
            shift_x = -0.5
        if round(current_state[1],5) < 0:
            shift_y = -0.02
        plt.arrow(0,0,current_state[0]*0.92,current_state[1]*0.92,head_width=0.04,head_length=0.08, color ='b')

        plt.text(current_state[0]*1.02 + shift_x, current_state[1]*1.02+shift_y,'|current state>')
        plt.arrow(angle[0],angle[1],angle_cont[0],angle_cont[1],linestyle='dotted',color='red')
        plt.arrow(angle_cont[0],angle_cont[1], angle[0],angle[1],linestyle='dotted',color='red')
        
        new_state = self.reflection(theta)
        
        plt.arrow(0,0,new_state[0]*0.92,new_state[1]*0.92,head_width=0.04,head_length=0.08, color ='b')

        plt.text(new_state[0]*1.02, new_state[1]*1.02+0.02,'|new state>')
        plt.show()

        

    #Probabilities of having 0 or 1 in the current state -- CORE            
    def prob(self):
        current_state = self.read_state()
        observe_prob = [round(current_state[0]**2,5),round(current_state[1]**2,5)]

        return observe_prob

    #Probabilities of having 0 or 1 in the current state -- READ 
    def probs_state(self):
        data = self.prob()
        self.text['state'] = tk.NORMAL
        self.text.insert(tk.END, '\nProbability of observing: ')
        self.text.insert(tk.END, f'state |0> is {data[0]}; state |1> {data[1]} for current quantum state')
        self.text['state'] = tk.DISABLED

    #Measurement based on probabilities and randomized normal distribution -- CORE
    def measure(self, number_of_shots):
        current_state_prob = self.prob()
        current_state_to_distribute = [round(current_state_prob[0],5)*100000, round(current_state_prob[1],5)*100000]
        result = {'0':0, '1':0}

        for i in range(number_of_shots):
            r = randrange(0,99999)
            
            if r < current_state_to_distribute[0]:
                result['0'] += 1
            else:
                result['1'] += 1
                
        return result

    #Measurement based on probabilities and randomized normal distribution -- READ
    def measure_state(self):
        input_data = self.measure_entry.get()
        shots = 0
        #Validation
        if input_data.isdigit() and int(input_data) >= 0:
            shots = int(input_data)
        else:
            self.text['state'] = tk.NORMAL
            self.text.insert(tk.END, '\nInput data for measurement is incorrect')
            self.text['state'] = tk.DISABLED
            return 0

        result = self.measure(shots)

        self.text['state'] = tk.NORMAL
        self.text.insert(tk.END, f'\nResult of {shots} observations is: ')
        self.text.insert(tk.END, f"'0':{result['0']}, '1':{result['1']} ")
        self.text['state'] = tk.DISABLED

        return result
        
    #Measurement plot based on probabilities and randomized normal distribution -- READ
    def plot_measure_state(self):
        data = self.measure_state()
        #Validation
        if data == 0:
            return

        x = ('0', '1')
        y = (data['0'], data['1'])
        plt.figure(figsize=[6,6])
        plt.bar(x,y,align='center') # A bar chart
        plt.xlabel('Outcome')
        plt.ylabel('Result total')
        
        plt.text(0, y[0], str(y[0]))
        plt.text(1, y[1], str(y[1]))
        
        plt.show()

    #shifting bases TO theta, not BY theta, also shifting visited states by theta -- CORE
    def change_basis(self, theta):
        
        check = theta
        previous = self.__basis_theta[-1]
        if check > 360:
            times = check//360
            check = round(check - times*360,5)
        if check == self.__basis_theta[-1]:
            raise Exception('The basis remained the same')
        init_basis = self.__basis[0]
        self.__basis_theta.append(check)
        radian = (theta * pi) / 180
        R = [
        [cos(radian), -1*sin(radian)],
        [sin(radian), cos(radian)]
        ]
        new_basis = self.__linear_evolve(R,init_basis)

        self.__basis.append(new_basis)
        
        difference = check - previous
        radian = (difference * pi) / 180
        R = [
            [cos(radian), -1*sin(radian)],
            [sin(radian), cos(radian)]
            ]
        #print(difference)
        for i in range (len(self.__quantum_states)):
            new_rotation = self.__linear_evolve(R,self.__quantum_states[i])
            self.__quantum_states[i] = new_rotation

        radian = pi / 2
        R = [
            [cos(radian), -1*sin(radian)],
            [sin(radian), cos(radian)]
            ]

        j = (new_basis, self.__linear_evolve(R,new_basis))
        return j

    #Basis shifting -- READ
    def change_basis_wrap(self):
        input_data = self.change_basis_entry.get()
        theta = 0

        #Validation
        if input_data.isdigit() and int(input_data) >= 0 and int(input_data) <= 360:
            theta = int(input_data)
        else:
            self.text['state'] = tk.NORMAL
            self.text.insert(tk.END, '\nInput data for basis change is incorrect')
            self.text['state'] = tk.DISABLED
            return
        try:
            new_basis = self.change_basis(theta)
            self.text['state'] = tk.NORMAL
            self.text.insert(tk.END, f'\nNew basis coordinates are: x ({round(new_basis[0][0],5)}; {round(new_basis[0][1],5)}), y ({round(new_basis[1][0],5)}; {round(new_basis[1][1],5)})')
            self.text['state'] = tk.DISABLED
            self.button_draw_state_prev_basis.state(["!disabled"])
            self.button_remove_basis.state(["!disabled"])
            self.button_prob_two_basis.state(["!disabled"])

        except:
            self.text['state'] = tk.NORMAL
            self.text.insert(tk.END, '\nBasis remained the same')
            self.text['state'] = tk.DISABLED
            return

    #draws last (current) state in both bases systems - current and previous -- READ
    def draw_state_in_previous_basis(self):
        if len(self.__basis) < 2:
            raise Exception('There is only one basis in the system')
        else:

            self.__draw_unit_circle(-2, f'Previous basis of {self.__basis_theta[-2]}\N{DEGREE SIGN} - x axis')
            
            previous = self.__basis_theta[-2]
            current = self.__basis_theta[-1]
            difference = previous - current
            
            radian = (difference * pi) / 180
            
            R = [
            [cos(radian), -1*sin(radian)],
            [sin(radian), cos(radian)]
            ]
            
            previous_state = self.__linear_evolve(R,self.read_state())
            
            shift_y = 0.02
            shift_x = 0
            if round(previous_state[0],5) < 0:
                shift_x = -0.5
            if round(previous_state[1],5) < 0:
                shift_y = -0.02
            plt.arrow(0,0,previous_state[0]*0.92,previous_state[1]*0.92,head_width=0.04,head_length=0.08, color ='b')

            plt.text(previous_state[0]*1.02 + shift_x, previous_state[1]*1.02+shift_y,'|current state>')
            plt.show()

    #Probabilities of seeing basic states in 2 bases - current and previous -- READ
    def prob_in_both_states(self):
        if len(self.__basis) < 2:
            raise Exception('There is only one basis in the system')
        else:
            basis = self.__basis[-1]
            state_zero_current = [round(basis[0],5), round(basis[1],5)]

            radian = pi/2
        
            R = [
            [cos(radian), -1*sin(radian)],
            [sin(radian), cos(radian)]
            ]
            
            state_one_current = self.__linear_evolve(R,basis)
            
            self.text['state'] = tk.NORMAL
            self.text.insert(tk.END, f'\nCurrent basis: \nstate |0>  probabability to observe 0 is {round(state_zero_current[0]**2,5)}; ')
            self.text.insert(tk.END, f'probabability to observe 1 is {round(state_zero_current[1]**2,5)}')
            self.text.insert(tk.END, f'\nstate |1> probabability to observe 0 is {round(state_one_current[0]**2,5)}; ')
            self.text.insert(tk.END, f'probabability to observe 1 is {round(state_one_current[1]**2,5)}')
            
            basis_prev = self.__basis[-2]
            state_zero_prev = [round(basis_prev[0],5), round(basis_prev[1],5)]

            radian = pi/2
        
            R = [
            [cos(radian), -1*sin(radian)],
            [sin(radian), cos(radian)]
            ]
            
            state_one_prev = self.__linear_evolve(R,basis_prev)

            self.text.insert(tk.END, f'\nPrevious basis: \nstate |0> probabability to observe 0 is {round(state_zero_prev[0]**2,5)}')
            self.text.insert(tk.END, f'probabability to observe 1 is {round(state_zero_prev[1]**2,5)}')
            self.text.insert(tk.END, f'\nstate |1> probabability to observe 0 is {round(state_one_prev[0]**2,5)}; ')
            self.text.insert(tk.END, f'probabability to observe 1 is {round(state_one_prev[1]**2,5)}')
            self.text['state'] = tk.DISABLED
    
    #deletes last basis and reverts rotation of visited quantum states -- READ
    def take_back_basis_change(self):
        if len(self.__basis) < 2:
            pass
        else:
            if len(self.__basis) == 2:
                self.button_remove_basis.state(["disabled"])
                self.button_prob_two_basis.state(["disabled"])
                self.button_draw_state_prev_basis.state(["disabled"])

            deleted_basis = self.__basis.pop()
            deleted_basis_theta = self.__basis_theta.pop()
            
            current_basis_theta = self.__basis_theta[-1]
            
            difference = current_basis_theta - deleted_basis_theta
            radian = (difference * pi) / 180
            R = [
                [cos(radian), -1*sin(radian)],
                [sin(radian), cos(radian)]
                ]
        
            for i in range (len(self.__quantum_states)):
                rotation_takeback = self.__linear_evolve(R,self.__quantum_states[i])
                self.__quantum_states[i] = rotation_takeback

        self.text['state'] = tk.NORMAL
        self.text.insert(tk.END, f'\nState basis of {deleted_basis_theta} degrees was deleted')
        self.text['state'] = tk.DISABLED

    #Save current quantum analysis progress -- MENU
    def save_as(self):
        files = [('Quantum simulator state files', '*.qssf')] 
        file_path = tk.filedialog.asksaveasfilename(filetypes = files, defaultextension = files) 
        if file_path == '':
            return
        date_to_save = (self.__quantum_states, self.__basis, self.__basis_theta)
        saving = pickle.dumps(date_to_save)
        with open(file_path, 'wb') as f:
                f.write(saving) 

    #Save current history -- MENU
    def save_history_as(self):
        files = [('Plain text', '*.txt')] 
        file_path = tk.filedialog.asksaveasfilename(filetypes = files, defaultextension = files) 
        if file_path == '':
            return
        date_to_save = (self.text.get("1.0", "end"))
        with open(file_path, 'wt') as f:
                f.write(date_to_save) 

    #Load saved quantum progress -- MENU
    def load(self):
        files = [('Quantum simulator state files', '*.qssf')] 
        file_path = tk.filedialog.askopenfilename(filetypes = files, defaultextension = files) 
        if file_path == '':
            return
        content = None
        with open(file_path, 'rb') as f:
            content = f.read() 
        unpickled_data = pickle.loads(content)
        
        #print(unpickled_data[0])
        #print('\n')
        #print(unpickled_data[1])
        #print(unpickled_data[2])
        #print('YES')

        self.__quantum_states = unpickled_data[0]
        self.__basis = unpickled_data[1]
        self.__basis_theta = unpickled_data[2]

        if unpickled_data[0] == []:
            self.__change_load_reverse()

        else:
            self.__change_after_creation()
            if len(self.__basis) > 1:
                self.button_draw_state_prev_basis.state(["!disabled"])
                self.button_remove_basis.state(["!disabled"])
                self.button_prob_two_basis.state(["!disabled"])

        self.text['state'] = tk.NORMAL
        self.text.delete('1.0', tk.END)
        self.text.insert(tk.END, f'File "{file_path}" was loaded')
        self.text['state'] = tk.DISABLED

    #Chart with X values -- MENU
    def plot_x(self):
        if len(self.__quantum_states) < 1:
            self.error_state()
            return
        fig, ax = plt.subplots()
        x = []
        y = []

        for index in range(len(self.__quantum_states)):
            y.append(round(self.__quantum_states[index][0],5))
            x.append(index)

        ax.plot(x, y, marker='o', color='b')
        ax.set(xlabel='Number of state', ylabel='X value',
            title='X values of all quantum states')
        ax.grid()
        plt.show()

    #Chart with Y values -- MENU
    def plot_y(self):
        if len(self.__quantum_states) < 1:
            self.error_state()
            return
        fig, ax = plt.subplots()
        x = []
        y = []

        for index in range(len(self.__quantum_states)):
            y.append(round(self.__quantum_states[index][1],5))
            x.append(index)

        ax.plot(x, y, marker='o', color='b')
        ax.set(xlabel='Number of state', ylabel='Y value',
            title='Y values of all quantum states')
        ax.grid()
        plt.show()

    #Chart with X probability values -- MENU
    def plot_x_probs(self):
        if len(self.__quantum_states) < 1:
            self.error_state()
            return
        fig, ax = plt.subplots()
        x = []
        y = []

        for index in range(len(self.__quantum_states)):
            y.append(round(self.__quantum_states[index][0]**2,5))
            x.append(index)

        ax.plot(x, y,  marker='o', color='b')
        ax.set(xlabel='Number of state', ylabel='X probability',
            title='Probability of observing 0')
        ax.grid()
        plt.show()

    #Chart with Y probability values -- MENU
    def plot_y_probs(self):
        if len(self.__quantum_states) < 1:
            self.error_state()
            return
        fig, ax = plt.subplots()
        x = []
        y = []

        for index in range(len(self.__quantum_states)):
            y.append(round(self.__quantum_states[index][1]**2,5))
            x.append(index)

        ax.plot(x, y,  marker='o', color='b')
        ax.set(xlabel='Number of state', ylabel='Y probability',
            title='Probability of observing 1')
        ax.grid()
        plt.show()

    #Chart with X and Y values -- MENU
    def plot_x_y(self):
        if len(self.__quantum_states) < 1:
            self.error_state()
            return
        fig, ax = plt.subplots()
        x_x = []
        y_x = []
        y_y = []
        for index in range(len(self.__quantum_states)):
            y_x.append(round(self.__quantum_states[index][0],5))
            y_y.append(round(self.__quantum_states[index][1],5))
            x_x.append(index)

        ax.plot(x_x, y_x, marker='o', color='b', label="X values")
        ax.plot(x_x, y_y, color='orange', marker='o', label="Y values")
        ax.set(xlabel='Number of state', title='X and Y values of all quantum states')
        ax.legend()
        ax.grid()
        plt.show()

    #Chart with X and Y probability values -- MENU
    def plot_x_y_probs(self):
        if len(self.__quantum_states) < 1:
            self.error_state()
            return
        fig, ax = plt.subplots()
        x_x = []
        y_x = []
        y_y = []
        for index in range(len(self.__quantum_states)):
            y_x.append(round(self.__quantum_states[index][0]**2,5))
            y_y.append(round(self.__quantum_states[index][1]**2,5))
            x_x.append(index)

        ax.plot(x_x, y_x, marker='o', color='b', label="X probability")
        ax.plot(x_x, y_y, color='orange', marker='o', label="Y probability")
        ax.set(xlabel='Number of state', title='X and Y probabilities of all quantum states')
        ax.legend()
        ax.grid()
        plt.show()
    
    #Error message for plots when system is new -- MENU
    def error_state(self):
        tk.messagebox.showerror('Error', 'No quantum state in the system')

    def plot_x_distribution(self):
        if len(self.__quantum_states) < 1:
            self.error_state()
            return
        fig, ax = plt.subplots()
        y = []
        for index in range(len(self.__quantum_states)):
            y.append(round(self.__quantum_states[index][0],2))
        ax.hist(y, ec='black')
        plt.show()

    def plot_y_distribution(self):
        if len(self.__quantum_states) < 1:
            self.error_state()
            return
        fig, ax = plt.subplots()
        y = []
        for index in range(len(self.__quantum_states)):
            y.append(round(self.__quantum_states[index][1],2))
        ax.hist(y, ec='black')
        plt.show()
        

    #Create new simulation -- MENU
    def new(self, parent):
        MsgBox = tk.messagebox.askquestion ('Quantum simulator','Are you sure you want to create new simulation',icon = 'warning')
        if MsgBox == 'yes':
            MsgBox2 = tk.messagebox.askquestion ('Save progress','Do you want to save progress?',icon = 'warning')
            if MsgBox2 == 'yes':
                self.save_as()
            parent.show_frame(Initial_choice)
            self.__quantum_states = []
            self.__basis = [[1,0]]
            self.__basis_theta = [0]
            self.__change_load_reverse()
            self.text['state'] = tk.NORMAL
            self.text.delete('1.0', tk.END)
            self.text.insert(tk.END, 'Here will be showed the history of actions taken in the quantum simulation')
            self.text['state'] = tk.DISABLED

    #Current quantum system info -- MENU
    def system_info(self):
        if len(self.__quantum_states) < 1:
            tk.messagebox.showinfo('Quantum system information', 'The system not exists yet')
        else:
            tk.messagebox.showinfo('Quantum system information', f'Quantum system has {len(self.__quantum_states)} states and {len(self.__basis)} basis')

    #Delete any state -- MENU
    def delete_state(self):
        if len(self.__quantum_states) < 2:
             tk.messagebox.showerror('Delete quantum state', 'Number of states cannot go below 1')
             return

        states = tk.simpledialog.askinteger("Delete quantum state", f"Total number of states is {len(self.__quantum_states)}. Select state to delete:")

        if states > len(self.__quantum_states) or states < 1:
             tk.messagebox.showerror('Delete quantum state', 'State to delete cannot be more than number of states or less than 1')
             return
        else:
            self.__quantum_states.pop(states-1)
            self.text['state'] = tk.NORMAL
            self.text.insert(tk.END, f'\nQuantum state number {states} was deleted')
            self.text['state'] = tk.DISABLED


class Classical_simulator(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #Lists for classical system parameters -- CORE
        self.bit_states = []
        self.system_state = []
        
        label = tk.Label(self, text="Classical system functions")
        label.grid(row=0, column=0,columnspan=2, sticky="nsew")
        #Text field for log -- Text field, diasabled + scrollbar
        self.text = tk.Text(self, width = 100)
        self.text.grid(row=0, column=7, columnspan=55, rowspan=55, padx=20, pady=20, sticky="e")
        scrollb = ttk.Scrollbar(self, command=self.text.yview)
        scrollb.grid(row=0, column=7, columnspan=55, rowspan=55, padx=20, pady=20, sticky="nse")
        self.text['yscrollcommand'] = scrollb.set

        self.text.insert(tk.END, 'Here will be showed the history of actions taken in the classical simulation')
        self.text['state'] = tk.DISABLED

        #Add new bit -- Button + field
        self.button_new_bit = ttk.Button(self, text="Add new bit", command=self.add_a_new_bit)
        self.new_bit_system_entry = ttk.Entry(self)
        self.button_new_bit.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.new_bit_system_entry.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        #System state vector -- Button
        self.button_system_vector = ttk.Button(self, text="State vector", command=self.print_state_vector)
        self.button_system_vector.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

        #System state  -- Button
        self.button_system_state = ttk.Button(self, text="State vector", command=self.print_state)
        self.button_system_state.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

        #NOT operator over selected bit  -- Button + field
        self.button_not = ttk.Button(self, text="NOT operator", command=self.not_op)
        self.not_entry = ttk.Entry(self)
        self.button_not.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")
        self.not_entry.grid(row=4, column=1, padx=5, pady=5, sticky="nsew")

        #CNOT operator over selected bit  -- Button + field x2
        self.button_cnot = ttk.Button(self, text="CNOT operator", command=self.cnot)
        self.cnot_entry_c = ttk.Entry(self)
        self.cnot_entry_t = ttk.Entry(self)
        
        self.button_cnot.grid(row=5, column=0, padx=5, pady=5, rowspan=2, sticky="nsew")
        self.cnot_entry_c.grid(row=5, column=1, padx=5, pady=5, sticky="nsew")
        self.cnot_entry_t.grid(row=6, column=1, padx=5, pady=5, sticky="nsew")

        #initial state
        self.__add_a_new_bit_initial()

    #Top menu for classical simulator -- MENU
    def menubar(self, parent):
        menubar = tk.Menu(parent)
        pageMenu = tk.Menu(menubar)
        pageMenu.add_command(label="New", command= lambda: (self.new(parent)))
        pageMenu.add_command(label="Save as", command=self.save_as)
        pageMenu.add_command(label="Save history as", command=self.save_history_as)
        pageMenu.add_command(label="Load", command=self.load)
        pageMenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=pageMenu)

        operatorMenu = tk.Menu(menubar)
        operatorMenu.add_command(label="NOT matrix", command=self.not_mat_gen)
        operatorMenu.add_command(label="CNOT matrix", command=self.cnot_mat_gen)
        operatorMenu.add_command(label="Delete state", command=self.delete_bit)
        menubar.add_cascade(label="Operators", menu=operatorMenu)

        
        return menubar

    #Validation of input field to have float
    def validate_entry(self, entry):
        result = re.match(r"\d+(.\d+)?$", entry)
        return result is not None

    #Add new bit to system -- CORE + READ
    def add_a_new_bit(self):
        input_data = self.new_bit_system_entry.get()
            
        if self.validate_entry(input_data):
            try:
                state_value = float(input_data)
            except:
                self.add_message(f'Wrong input data for new bit')
                return

            if state_value < 0 or state_value > 1:
                self.add_message(f'Wrong input data for new bit')
                return
        else:
            if input_data == '' or input_data.isdigit()==False or int(input_data) < 0 or int(input_data) > 1:
                self.add_message(f'Wrong input data for new bit')
                return
            if input_data != '' and input_data.isdigit() and int(input_data) >= 0 and int(input_data) <= 1:
                state_value = int(input_data)
        new_bit_state = []

        bit_value = state_value
        complement_bit_value = 1 - bit_value
        new_bit_state.append(complement_bit_value)
        new_bit_state.append(bit_value)
            
        self.bit_states.append(new_bit_state)
        self.add_message(f'New bit with {new_bit_state} state was added to system')
        tensor_result = [self.system_state, new_bit_state]
        self.system_state = self.__vector_tensor_product(tensor_result)

    #Set initial bit to [0.5, 0.5] -- CORE + READ
    def __add_a_new_bit_initial(self, state_value = 0.5):
        new_bit_state = []
        bit_value = state_value
        complement_bit_value = 1 - bit_value
        new_bit_state.append(complement_bit_value)
        new_bit_state.append(bit_value)    
        self.bit_states.append(new_bit_state)
        self.add_message(f'Initial bit of the system {new_bit_state}')
        self.system_state = self.__vector_tensor_product(self.bit_states)
        

    #Tensor product -- CORE
    def __vector_tensor_product(self, bit_states):
        result = bit_states[0]
        flag = False
        vector_A = []
        vector_B = []
        
        for bit_state in bit_states:
            vector_temp = []
            if flag == False:
                vector_A = bit_state
                flag = True
            else:
                vector_B = bit_state
            
                for i in range(len(vector_A)):
                    for j in range(len(vector_B)):
                        vector_temp.append(vector_A[i] * vector_B[j])
                vector_A = vector_temp
        result = vector_A
        return result


    #Current state vector -- READ
    def print_state_vector(self):

        self.add_message(f'System state vector is: {self.system_state}')
        return self.system_state

    #Generalization of adding messages -- READ
    def add_message(self, text):
        self.text['state'] = tk.NORMAL
        self.text.insert(tk.END, '\n'+text)
        self.text['state'] = tk.DISABLED
    
    #Current state -- READ
    def print_state(self):
        bits = len(self.bit_states)
        bits_comb = list(product([0, 1], repeat=bits))
        states = self.system_state
        self.add_message('State of the system as a linear combination of the basis states:')
        for index in range(len(states)):
            if states[index] != 0:
                string_tuple = ''
                for num in bits_comb[index]:
                    string_tuple += str(num)
                self.add_message(f'[{string_tuple}] {states[index]}')

    #linear evolve -- CORE
    def __linear_evolve(self,probabilistic_operator, probabilistic_state):
        result = []
        for i in range(len(probabilistic_operator)):
            summation = 0
            for j in range(len(probabilistic_operator[0])):
                summation += probabilistic_operator[i][j]*probabilistic_state[j]
            result.append(summation)
        probabilistic_state = result
        return result
    
    #Applying NOT to specified bit, changing it in the bit_states and recalculating the system_state -- CORE + READ
    def not_op(self):
        input_data = self.not_entry.get()
        if input_data.isdigit() and int(input_data) > 0 and int(input_data) <= len(self.bit_states):
            index_of_bit = int(input_data)
        else:
            self.add_message('Wrong data provided to NOT operator')
            return

        not_operator = self._not_gen(index_of_bit)
        self.add_message(f'NOT operator was applied on {input_data} bit')
        self.system_state = self.__linear_evolve(not_operator,self.system_state)
        
    #Not operator generator  -- CORE  
    def _not_gen(self, target_bit, total_size = -1):
        bits = len(self.bit_states)
        if total_size != -1:
            bits = total_size
        
        dims = 2**bits
        result = []
        t_bit_index = target_bit - 1
        bits_comb = list(product([0, 1], repeat=bits))
        indeces = []
        indeces_2 = []
        for i in range(dims):
            result.append([])
            string = ''
            for k in range(len(bits_comb[0])):
                string += str(bits_comb[i][k])
            indeces.append(string)
            indeces_2.append(string)

            for j in range(dims):
                result[i].append(0)
        new_indeces = []

        for j in range(len(result[0])):
            was = list(indeces[j])
            will = was
            if was[t_bit_index] == '0':
                will[t_bit_index] = '1'
            else:
                will[t_bit_index] = '0'
            y = str("".join(will))
            new_indeces.append(y)
        for i in range(dims):
            result[int(indeces[i],2)][int(new_indeces[i],2)] = 1
        #print(result)
        return result

    #CCNOT operator generator  -- CORE  + READ
    def cnot(self, c = 0, t = 0, length = 0):
        if c != 0:
            control_bit = c
            target_bit = t
            dims = 2**length
        else:
            input_1 = self.cnot_entry_c.get()
            input_2 = self.cnot_entry_t.get()
            if input_1.isdigit() and int(input_1) > 0 and int(input_1) <= len(self.bit_states) and input_2.isdigit() and int(input_2) > 0 and int(input_2) <= len(self.bit_states) and int(input_1)!= int(input_2):
                control_bit = int(input_1)
                target_bit = int(input_2)
            else:
                self.add_message('Wrong data provided to CNOT operator')
                return

            dims = 2**len(self.bit_states)
        result = []
        c_bit_index = control_bit - 1
        t_bit_index = target_bit - 1
        if c != 0:
            bits_comb = list(product([0, 1], repeat=length))
        else:
            bits_comb = list(product([0, 1], repeat=len(self.bit_states)))
        indeces = []
        indeces_2 = []
        for i in range(dims):
            result.append([])
            string = ''
            for k in range(len(bits_comb[0])):
                string += str(bits_comb[i][k])
            indeces.append(string)
            indeces_2.append(string)
            for j in range(dims):
                result[i].append(0)

        for i in range(dims):
            if indeces[i][c_bit_index] == '1':
                #print(indeces[i])
                #if c_bit_index < t_bit_index:
                if indeces[i][t_bit_index] == '0':
                    new_index = indeces[i][:t_bit_index]+'1'+indeces[i][t_bit_index+1:]
                else:
                    new_index = indeces[i][:t_bit_index]+'0'+indeces[i][t_bit_index+1:]
                indeces_2[i] = new_index
        for i in range(dims):
            result[int(indeces_2[i],2)][int(indeces[i],2)] = 1
        
        if c != 0:
            return result
        apply = self.__linear_evolve(result,self.system_state)
        self.system_state = apply
        self.add_message(f'CNOT operator was applied on {target_bit} bit based on value of {control_bit} bit (control)')
        return apply

    #Save current quantum analysis progress -- MENU
    def save_as(self):
        files = [('Classical simulator state files', '*.cssf')] 
        file_path = tk.filedialog.asksaveasfilename(filetypes = files, defaultextension = files) 
        if file_path == '':
            return
        date_to_save = (self.bit_states, self.system_state)
        saving = pickle.dumps(date_to_save)
        with open(file_path, 'wb') as f:
                f.write(saving) 

    #Save current history -- MENU
    def save_history_as(self):
        files = [('Plain text', '*.txt')] 
        file_path = tk.filedialog.asksaveasfilename(filetypes = files, defaultextension = files) 
        if file_path == '':
            return
        date_to_save = (self.text.get("1.0", "end"))
        with open(file_path, 'wt') as f:
                f.write(date_to_save) 

    #Load saved quantum progress -- MENU
    def load(self):
        files = [('Classical simulator state files', '*.cssf')] 
        file_path = tk.filedialog.askopenfilename(filetypes = files, defaultextension = files) 
        if file_path == '':
            return
        content = None
        with open(file_path, 'rb') as f:
            content = f.read() 
        unpickled_data = pickle.loads(content)

        self.bit_states  =  unpickled_data[0]
        self.system_state = unpickled_data[1]

        self.text['state'] = tk.NORMAL
        self.text.delete('1.0', tk.END)
        self.text.insert(tk.END, f'File "{file_path}" was loaded')
        self.text['state'] = tk.DISABLED

    #Create new simulation -- MENU
    def new(self, parent):
        MsgBox = tk.messagebox.askquestion ('Classical simulator','Are you sure you want to create new simulation',icon = 'warning')
        if MsgBox == 'yes':
            MsgBox2 = tk.messagebox.askquestion ('Save progress','Do you want to save progress?',icon = 'warning')
            if MsgBox2 == 'yes':
                self.save_as()
            parent.show_frame(Initial_choice)
            self.bit_states = []
            self.system_state = []
            self.text['state'] = tk.NORMAL
            self.text.delete('1.0', tk.END)
            self.text.insert(tk.END, 'Here will be showed the history of actions taken in the classical simulation')
            self.__add_a_new_bit_initial()
            self.text['state'] = tk.DISABLED
    
    #NOT matrix -- READ
    def not_mat_gen(self):
        bits = tk.simpledialog.askinteger("NOT generator", "Enter the total number of bits:")
        if not bits or bits <= 0:
            tk.messagebox.showerror('NOT generator', 'The total number of bits must be inserted and it should be positive')
            return
        control = tk.simpledialog.askinteger("NOT generator", "Enter the position of bit to which NOT should be applied:")

        if not control or control <= 0 or control > bits:
            tk.messagebox.showerror('NOT generator', 'The position of bit to which NOT should be applied must be inserted, it should be positive and not exceed the total number of bits')
            return

        result = self._not_gen(control, bits)
        self.add_message(f'NOT operator matrix for {bits} bits, where NOT applied to {control} bit')
        for i in result:
            self.add_message(f'{i}')
    
    #CNOT matrix -- READ
    def cnot_mat_gen(self):
        bits = tk.simpledialog.askinteger("CNOT generator", "Enter the total number of bits:")
        if not bits or bits <= 1:
            tk.messagebox.showerror('CNOT generator', 'The total number of bits must be inserted, it should be higher than 1 and not exceed the total number of bits')
            return
        control = tk.simpledialog.askinteger("CNOT generator", "Enter the position of control bit:")

        if not control or control <= 0 or control > bits:
            tk.messagebox.showerror('CNOT generator', 'The position of control bit must be inserted, it should be positive and not exceed the total number of bits')
            return

        target = tk.simpledialog.askinteger("CNOT generator", "Enter the position of target bit:")

        if not target or target <= 0 or target > bits:
            tk.messagebox.showerror('CNOT generator', 'The position of tarhet bit must be inserted, it should be positive and not exceed the total number of bits')
            return

        result = self.cnot(control, target, bits)
        self.add_message(f'CNOT operator matrix for {bits} bits, where {control} is control bit and {target} is target bit')
        for i in result:
            self.add_message(f'{i}')

    #Delete any bit -- MENU
    def delete_bit(self):
        if len(self.bit_states) < 2:
             tk.messagebox.showerror('Delete classical bit', 'Number of bits cannot go below 1')
             return

        bit = tk.simpledialog.askinteger("Delete classical bit", f"Total number of bits is {len(self.bit_states)}. Select bit to delete:")
        
        if not bit:
            return

        if bit >len(self.bit_states) or bit < 1:
             tk.messagebox.showerror('Delete classical bit', 'Bit to delete cannot be more than number of bits or less than 1')
             return
        else:
            bits = len(self.bit_states)
            bits_comb = list(product([0, 1], repeat=bits))
            states = self.system_state

            new = { }

            for index in range(len(states)):
                if states[index] != 0:
                    string_tuple = ''
                    for num in range(len(bits_comb[index])):
                        if num != bit-1:
                            string_tuple += str(bits_comb[index][num])
                    if int(string_tuple,2) not in new:
                        new[int(string_tuple,2)] = states[index]
                    else: new[int(string_tuple,2)] += states[index]

            new_state = []
            values = new.keys()
            for i in range(2**(len(self.bit_states)-1)):
                if i not in values:
                    new_state.append(0)
                else:
                    new_state.append(new[i])
            self.bit_states.pop(bit-1)
            self.system_state = new_state
            self.add_message(f'Bit number {bit} was deleted and system is recalculated')
            #print (new_state)
            

#Application start-up
app = core_frame()
app.geometry("1180x620")
app.resizable(0, 0) 
app.mainloop()
