import tkinter as tk
from tkinter import ttk
from math import pi, sin, cos
import matplotlib.pyplot as plt
from random import randrange

#Core class for frames manipulation
class core_frame(tk.Tk):
    def __init__(self):
        
        tk.Tk.__init__(self)

        #tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "Simulator")
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Initial_choice, Quantum_simulator):
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
        button2 = ttk.Button(self, text="Quantum system",
                            command=lambda: controller.show_frame(Quantum_simulator))
        button2.pack()

    def menubar(self, parent):
        menubar = tk.Menu(parent)
        return menubar

#Quantum simulator frame
class Quantum_simulator(tk.Frame):

    #Lists for quantum system parameters -- CORE
    __quantum_states = []
    __basis = [[1,0]]
    __basis_theta = [0]

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Quantum system functions")
        label.grid(row=0, column=0,columnspan=2, sticky="nsew")
        #Initial function -- create system - Button + entry field
        self.button_new_system = ttk.Button(self, text="Create quantum system", command=self.__create_quantum_system)
        self.quantum_create_system_entry = ttk.Entry(self)
        self.button_new_system.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.quantum_create_system_entry.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        #Text field for log -- Text field, diasabled
        self.text = tk.Text(self, width = 70)
        self.text.grid(row=0, column=7, columnspan=55, rowspan=55, padx=20, pady=20, sticky="e")
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

    #This is a menu to save/load mostly
    def menubar(self, parent):
        menubar = tk.Menu(parent)
        pageMenu = tk.Menu(menubar)
        pageMenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=pageMenu)

        analysisMenu = tk.Menu(menubar)
        analysisMenu.add_command(label="Plot X", command=quit)
        analysisMenu.add_command(label="Plot Y", command=quit)
        analysisMenu.add_command(label="Plot X and Y", command=quit)
        analysisMenu.add_command(label="Plot X distribution", command=quit)
        analysisMenu.add_command(label="Plot Y distribution", command=quit)
        menubar.add_cascade(label="Analysis", menu=analysisMenu)

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
            self.text.insert(tk.INSERT, '\nInput data for initial quantum state is incorrect')
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
        self.text.insert(tk.INSERT, '\nInitial quantum state is: ')
        self.text.insert(tk.INSERT, f'|0> {round(self.__quantum_states[-1][0],5)}; |1> {round(self.__quantum_states[-1][1],5)}')
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

    #Current quantum state -- CORE
    def read_state(self):
        return self.__quantum_states[-1]

    #Display current quantum state -- READ
    def read_current_state(self):

        current_state = self.read_state()
        self.text['state'] = tk.NORMAL    
        self.text.insert(tk.INSERT, '\nCurrent quantum state is: ')
        self.text.insert(tk.INSERT, f'|0> {round(current_state[0],5)}; |1> {round(current_state[1],5)}')
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
        else:
            self.text['state'] = tk.NORMAL
            self.text.insert(tk.INSERT, '\nInput data for rotation is incorrect')
            self.text['state'] = tk.DISABLED
            return

        self.rotation(theta)
        self.text['state'] = tk.NORMAL
        self.text.insert(tk.INSERT, f'\nQuantum state was rotated by: {theta} degrees')
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
            self.text.insert(tk.INSERT, '\nInput data for reflection is incorrect')
            self.text['state'] = tk.DISABLED
            return

        self.reflection(theta)
        self.text['state'] = tk.NORMAL
        self.text.insert(tk.INSERT, f'\nQuantum state was reflected by: {theta} degrees')
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
            self.text.insert(tk.INSERT, '\nInput data for reflection is incorrect')
            self.text['state'] = tk.DISABLED
            return

        self.text['state'] = tk.NORMAL
        self.text.insert(tk.INSERT, f'\nQuantum state was reflected by: {theta} degrees')
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
        self.text.insert(tk.INSERT, '\nProbability of observing: ')
        self.text.insert(tk.INSERT, f'state |0> is {data[0]}; state |1> {data[1]} for current quantum state')
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
            self.text.insert(tk.INSERT, '\nInput data for measurement is incorrect')
            self.text['state'] = tk.DISABLED
            return

        result = self.measure(shots)

        self.text['state'] = tk.NORMAL
        self.text.insert(tk.INSERT, f'\nResult of {shots} observations is: ')
        self.text.insert(tk.INSERT, f"'0':{result['0']}, '1':{result['1']} ")
        self.text['state'] = tk.DISABLED

        return result
        
    #Measurement plot based on probabilities and randomized normal distribution -- READ
    def plot_measure_state(self):
        data = self.measure_state()
        x = ('0', '1')
        y = (data['0'], data['1'])
        plt.figure(figsize=[6,6])
        plt.bar(x,y,align='center') # A bar chart
        plt.xlabel('Outcome')
        plt.ylabel('Result total')
        
        plt.text(0, y[0], str(y[0]))
        plt.text(1, y[1], str(y[1]))
        
        plt.show()


#Application start-up
app = core_frame()
app.geometry("920x720")
app.resizable(0, 0) 
app.mainloop()