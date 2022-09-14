
# hiring professors and replace the retired ones with the same number and gender 
#0 stands for female and 1 stands for males.
# plot 1.number of M and F
# plot average salary
# plot average increment


#import the libraries
from operator import mod
import sched
from statistics import mode
from mesa import Agent, Model
import random
from mesa.time import BaseScheduler, RandomActivation
import matplotlib.pyplot as plt
import numpy as np


Unique_ID = 0

#unique ID
random.seed(5)

def unique_ID():
    global Unique_ID
    Unique_ID += 1
    return Unique_ID

#Initial creating of professors and defining each step


class ProfAgent(Agent):
    """ An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.gender = -1
        self.salary = 100000
        self.current_year = 0
        self.years_employed = 0
        self.rank = 1
        self.maternal=0
        self.leave = 0
        

    # each step

    def step(self):
        
       
       
        self.years_employed += 1
        if self.years_employed<21:
            self.salary += 3000
          
        self.current_year += 1


class ProfModel(Model):
    def __init__(self, percentFemale_assistant,  percentFemale_associate,  percentFemale_full,   hiring_employee_female_percent,  probability_of_promotion_to_the_associate_professor,  probability_of_promotion_to_the_full_professor,num_awards,num_quitters):
        self.percentFemale_assistant = percentFemale_assistant
        self.percentFemale_associate = percentFemale_associate
        self.percentFemale_full = percentFemale_full
        self.hiring_employee_female_percent = hiring_employee_female_percent
        self.probability_of_promotion_to_the_full_professor = probability_of_promotion_to_the_full_professor
        
        self.probability_of_promotion_to_the_associate_professor =probability_of_promotion_to_the_associate_professor
        self.num_awards = num_awards
        self.num_quitters = num_quitters
        self.num_increments_assistant = 6
        self.schedule = BaseScheduler(self)
        self.active_professors = []
        self.assistant_professors_income = []
    # model.creating_agents(500, 300, 200)
    # creating collection of assistant/associate/full professors and define their salary/years_employed and add them to the schedule
    def creating_agents(self, number_of_assistant, number_of_associate, number_of_full):

        self.number_of_assistant = number_of_assistant
        self.number_of_associate = number_of_associate
        self.number_of_full = number_of_full
        
        for each_number in range(self.number_of_assistant):
            agent = ProfAgent(unique_ID(), self)
            agent.rank = 1
            if random.random()<self.percentFemale_assistant:
                agent.gender = 0
                agent.salary = 100000
                agent.maternal=0
                agent.leave=0
                
            else:
                
                agent.gender = 1
                
                
            
            self.active_professors.append(agent)
        
        for each_number in range(self.number_of_associate):
            
            agent = ProfAgent(unique_ID(), self)
            agent.rank = 2
            if random.random() <= self.percentFemale_associate:
                agent.gender = 0
                agent.salary = 100000
                agent.maternal=0
                agent.leave=0
                
                
            else:
                agent.gender = 1
                
                
            
            self.active_professors.append(agent)
        

        for each_number in range(self.number_of_full):
            agent = ProfAgent(unique_ID(), self)
            agent.rank = 3
            if random.random() <= self.percentFemale_full:
                agent.gender = 0
                agent.salary = 100000
                agent.maternal=0
                agent.leave=0
                
            else:
                agent.gender = 1
                
                
            
            self.active_professors.append(agent)
        
        
        
        
        #Setting years of services
        for each in range(self.number_of_assistant):
            self.active_professors[each].years_employed = each % 7
        for each in range(self.number_of_associate):
            self.active_professors[self.number_of_assistant +
                                   each].years_employed = 7+each % 7
        for each in range(0, self.number_of_full):
            self.active_professors[self.number_of_assistant +
                                   self.number_of_associate+each].years_employed = 14+each % 22
        
            
            
        #Setting salary of professors
        for each in range(self.number_of_assistant+self.number_of_associate+self.number_of_full):
            if self.active_professors[each].years_employed <= 20:
                self.active_professors[each].salary += (
                    3000 * self.active_professors[each].years_employed)
            else:
                self.active_professors[each].salary = 160000
        
               
        for each in self.active_professors:
            
            self.schedule.add(each)
# ---------------------------------------------------------------------------------------------------
        
    #Giving promotion to assistant and associate professors

    def promotion(self):
        # for each in self.schedule.agents:
        #     if  each.years_employed>35:
        #         print("eligible professors to got retired.",each.gender, each.salary, each.years_employed,each.rank)
        
        assistant_promoted_ones = []
        associate_promoted_ones = []
        retired_full_ones =[]
        promoted_assistant_professors = [
            each for each in self.schedule.agents if each.years_employed >6 and each.years_employed<14 and each.rank==1]
        promoted_associate_professors = [
            each for each in self.schedule.agents if each.years_employed >13 and each.rank==2 ]
        retired_full_professors = [each for each in self.schedule.agents if each.years_employed>35]
        
        # for each in promoted_associate_professors:
        #     print("probable associate ",each.unique_id,each.gender,each.maternal,each.leave)
                

                       
            
        for each_prof in promoted_assistant_professors:
            if random.random()<self.probability_of_promotion_to_the_associate_professor:
                each_prof.rank=2
                assistant_promoted_ones.append(each_prof)

        for each_prof in promoted_associate_professors:
            if random.random()<.6:
                each_prof.rank=3
                associate_promoted_ones.append(each_prof) 
            # if each_prof.gender==1:
            #     if random .random()<self.probability_of_promotion_to_the_full_professor_for_male:
            #         each_prof.rank=3
            #         associate_promoted_ones.append(each_prof)
            # elif each_prof.gender==0:
            #     if random.random()<self.probability_of_promotion_to_the_full_professor_for_female:
            #         each_prof.rank=3
                    # associate_promoted_ones.append(each_prof)
            # if random.random()<self.probability_of_promotion_to_the_full_professor:
            #     each_prof.rank=3
            #     associate_promoted_ones.append(each_prof)
            # if each_prof.gender==1:
                # print("male associate",each_prof.unique_id)
            # if random.random()<.6:
                # each_prof.rank=3
                # associate_promoted_ones.append(each_prof) 
                    # print("promoted male",each_prof.unique_id)
            # if each_prof.gender==0:
                # print("female associate",each_prof.unique_id,each_prof.maternal,each_prof.leave)
                # if each_prof.maternal==1 and each_prof.leave>=1:
                    # each_prof.leave-=1
                    # if each_prof.leave==0:
                        # each_prof.maternal=0
                    # print("after applying",each_prof.maternal,each_prof.leave)
                # if each_prof.maternal==0:
                    # if random.random()<.6:
                        # each_prof.rank=3
                        # associate_promoted_ones.append(each_prof) 
                        # print("promoted female",each_prof.unique_id)
                
        # male_retired=0
        # female_retired=0
        for each_prof in retired_full_professors:
        #     if each_prof.gender==0:
        #         female_retired+=1
        #     else:
        #         male_retired+=1
                
            
            retired_full_ones.append(each_prof)
            self.schedule.remove(each_prof)
            
        # print("retired ones",female_retired,male_retired)    
        return retired_full_ones

# -------------------------------------------------------------------------------------------------

    #hire new professors instead of quited and retired ones
    def hire_new_professors(self, retired_ones, quitted_ones):
        retired_ones = retired_ones
        quitted_ones = quitted_ones
        # for each in retired_ones:
        #     print("bazm retired",each.gender,each.years_employed,each.salary)
            
        # female=0
        # male=0    
        for each in quitted_ones+retired_ones:
            new_agent = ProfAgent(unique_ID(), self)
            # new_agent.gender = each.gender
            if random.random()<self.hiring_employee_female_percent:
                # female+=1
                new_agent.gender=0
                # new_agent.salary=100000
            else:
                # male+=1
                new_agent.gender=1
            new_agent.salary=100000
            self.schedule.add(new_agent)
        # print("hired",female,male)
# --------------------------------------------------------------------------------------------------------


    #special increment that is given to random professors
    def special_increment(self, num_awards):
        male_assistant=0
        female_assistant=0
        male_associate=0
        female_associate=0
        male_full=0
        female_full=0
        for each in self.schedule.agents:
            if each.rank==1:
                if each.gender==1:
                    male_assistant+=1
                else :
                    female_assistant+=1
            elif each.rank==2 :
                if each.gender==1:
                    male_associate+=1
                else:
                    female_associate+=1
            elif each.rank==3:
                if each.gender==1:
                    male_full+=1
                else:
                    female_full+=1
        
                
                
        lucky_professors = []
        eligible_professor = []
        for each in self.schedule.agents:
            if each.maternal==0:
                eligible_professor.append(each)
        lucky_professors = random.sample(eligible_professor, num_awards)
        for each in range(int(num_awards/4)):
            lucky_professors[each].salary += 1500
        for each in range(int(num_awards/4), int(2*num_awards/4)):
            lucky_professors[each].salary += 3000
        for each in range(int(2*num_awards/4), num_awards):
            lucky_professors[each].salary += 6000
# --------------------------------------------------------------------------------------------------

    #calculating the average of increment
    def average_number_of_increment(self):
        male_increment = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7 :0, 8 :0, 9: 0, 10 :0, 11 : 0, 12: 0, 13: 0 , 14: 0, 15: 0, 16: 0, 17: 0, 18: 0}
        female_increment = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7 :0, 8 :0, 9: 0, 10 :0, 11 : 0, 12: 0, 13: 0 , 14: 0, 15: 0, 16: 0, 17: 0, 18: 0}

        for each in self.schedule.agents:
            if each.years_employed == 0:
                if each.gender == 0:

                    female_increment[0] += 1
                else:
                    male_increment[0] += 1

            if each.years_employed == 1:
                if each.gender == 0:
                    female_increment[1] += 1

                else:
                    male_increment[1] += 1

            if each.years_employed == 2:
                if each.gender == 0:
                    female_increment[2] += 1

                else:
                    male_increment[2] += 1

            if each.years_employed == 3:
                if each.gender == 0:
                    female_increment[3] += 1

                else:
                    male_increment[3] += 1

            if each.years_employed == 4:
                if each.gender == 0:
                    female_increment[4] += 1

                else:
                    male_increment[4] += 1

            if each.years_employed == 5:
                if each.gender == 0:
                    female_increment[5] += 1

                else:
                    male_increment[5] += 1

            if each.years_employed == 6:
                if each.gender == 0:
                    female_increment[6] += 1

                else:
                    male_increment[6] += 1
            
            if each.years_employed == 7:
                if each.gender == 0:
                    female_increment[7] += 1

                else:
                    male_increment[7] += 1
            
            if each.years_employed == 8:
                if each.gender == 0:
                    female_increment[8] += 1

                else:
                    male_increment[8] += 1
            
            if each.years_employed == 9:
                if each.gender == 0:
                    female_increment[9] += 1

                else:
                    male_increment[9] += 1
            
            if each.years_employed == 10:
                if each.gender == 0:
                    female_increment[10] += 1

                else:
                    male_increment[10] += 1
            
            if each.years_employed == 11:
                if each.gender == 0:
                    female_increment[11] += 1

                else:
                    male_increment[11] += 1

            if each.years_employed == 12:
                if each.gender == 0:
                    female_increment[12] += 1

                else:
                    male_increment[12] += 1
            
            if each.years_employed == 13:
                if each.gender == 0:
                    female_increment[13] += 1

                else:
                    male_increment[13] += 1
            
            if each.years_employed == 14:
                if each.gender == 0:
                    female_increment[14] += 1

                else:
                    male_increment[14] += 1
            
            if each.years_employed == 15:
                if each.gender == 0:
                    female_increment[15] += 1

                else:
                    male_increment[15] += 1
            
            if each.years_employed == 16:
                if each.gender == 0:
                    female_increment[16] += 1

                else:
                    male_increment[16] += 1

            if each.years_employed == 17:
                if each.gender == 0:
                    female_increment[17] += 1

                else:
                    male_increment[17] += 1
            
            if each.years_employed == 18:
                if each.gender == 0:
                    female_increment[18] += 1

                else:
                    male_increment[18] += 1
            
            

        

        return((male_increment[1]*1 + male_increment[2]*2 + male_increment[3]*3+male_increment[4]*4+male_increment[5]*5+male_increment[6]*6
                )/(male_increment[0]+male_increment[1]+male_increment[2]+male_increment[3]+male_increment[4]+male_increment[5]+male_increment[6])),\
            ((female_increment[1]*1 + female_increment[2]*2 + female_increment[3]*3+female_increment[4]*4+female_increment[5]*5+female_increment[6]*6
              )/(female_increment[0]+female_increment[1]+female_increment[2]+female_increment[3]+female_increment[4]+female_increment[5]+female_increment[6])),\
                ((male_increment[7]*1 + male_increment[8]*2 + male_increment[9]*3+male_increment[10]*4+male_increment[11]*5+male_increment[12]*6
                )/(male_increment[7]+male_increment[8]+male_increment[9]+male_increment[10]+male_increment[11]+male_increment[12])),\
                ((female_increment[7]*1 + female_increment[8]*2 + female_increment[9]*3+female_increment[10]*4+female_increment[11]*5+female_increment[12]*6
              )/(female_increment[7]+female_increment[8]+female_increment[9]+female_increment[10]+female_increment[11]+female_increment[12])),\
                ((male_increment[13]*1 + male_increment[14]*2 + male_increment[15]*3+male_increment[16]*4+male_increment[17]*5+male_increment[18]*6
                )/(male_increment[13]+male_increment[14]+male_increment[15]+male_increment[16]+male_increment[17]+male_increment[18])),\
                 ((female_increment[13]*1 + female_increment[14]*2 + female_increment[15]*3+female_increment[16]*4+female_increment[17]*5+female_increment[18]*6
              )/(female_increment[13]+female_increment[14]+female_increment[15]+female_increment[16]+female_increment[17]+female_increment[18]))
                

            
# --------------------------------------------------------------------------------------------    

    #calculation of professors salary by their gender

    def average_salary_calculation(self):
        female_assistant_income = []
        male_assistant_income = []
        female_associate_income = []
        male_associate_income = []
        female_full_income = []
        male_full_income = []
        assistant_income = []
        associate_income = []
        full_income = []
        average_salary_of_female_assistant = 0
        average_salary_of_male_assistant = 0
        average_salary_of_assistant = 0
        average_salary_of_female_assistant = 0
        average_salary_of_female_associate = 0
        average_salary_of_male_associate = 0
        average_salary_of_associate = 0
        average_salary_of_female_Full = 0
        average_salary_of_male_Full = 0
        average_salary_of_full = 0

        for each in self.schedule.agents:

            if each.rank == 1:
                assistant_income.append(each.salary)
                if each.gender == 0:
                    female_assistant_income.append(each.salary)
                if each.gender==1:
                    male_assistant_income.append(each.salary)

            if each.rank == 2:
                associate_income.append(each.salary)
                if each.gender == 0:
                    female_associate_income.append(each.salary)
                elif each.gender == 1:
                    male_associate_income.append(each.salary)

            if each.rank == 3:
                full_income.append(each.salary)
                if each.gender == 0:
                    female_full_income.append(each.salary)
                if each.gender==1:
                    male_full_income.append(each.salary)

        
        if len(female_assistant_income)!=0:
            average_salary_of_female_assistant=sum(female_assistant_income)/len(female_assistant_income)
        elif len(female_assistant_income)==0:
            average_salary_of_female_assistant = 0
            
        if len(male_assistant_income)!=0:
            average_salary_of_male_assistant=sum(male_assistant_income)/len(male_assistant_income)
        elif len(male_assistant_income)==0:
            average_salary_of_male_assistant = 0
            
        if len(assistant_income)!=0:
            average_salary_of_assistant=sum(assistant_income)/len(assistant_income)
        elif len(assistant_income)==0:
            average_salary_of_ssistant = 0
        
        if len(female_associate_income)!=0:
            average_salary_of_female_associate=sum(female_associate_income)/len(female_associate_income)
        elif len(female_associate_income)==0:
            average_salary_of_female_associate = 0
            
            
        if len(male_associate_income)!=0:
            average_salary_of_male_associate=sum(male_associate_income)/len(male_associate_income)
        elif len(male_associate_income)==0:
            average_salary_of_male_associate = 0   
            
        if len(associate_income)!=0:
            average_salary_of_associate=sum(associate_income)/len(associate_income)
        elif len(associate_income)==0:
            average_salary_of_associate = 0   
            
        if len(female_full_income)!=0:
            average_salary_of_female_Full=sum(female_full_income)/len(female_full_income)
        elif len(female_full_income)==0:
            average_salary_of_female_Full = 0
            
        if len(male_full_income)!=0:
            average_salary_of_male_Full=sum(male_full_income)/len(male_full_income)
        elif len(male_full_income)==0:
            average_salary_of_male_Full = 0
            
        if len(full_income)!=0:
            average_salary_of_Full=sum(full_income)/len(full_income)
        elif len(full_income)==0:
            average_salary_of_Full = 0
            
            
            
        return average_salary_of_female_assistant,\
            average_salary_of_male_assistant,\
            average_salary_of_assistant,\
            average_salary_of_female_associate,\
            average_salary_of_male_associate,\
            average_salary_of_associate,\
            average_salary_of_female_Full,\
            average_salary_of_male_Full,\
            average_salary_of_Full
            
#--------------------------------------------------------------------------------------------------------------
    #Defining Quitters        
    def quitters(self,number_of_quitters):
        f_assis_quit = 0
        m_assis_quit = 0
        f_asso_quit = 0
        m_asso_quit = 0
        f_full_quit = 0
        m_full_quit = 0
        quitters = []
        quitters = random.sample(self.schedule.agents, number_of_quitters)
        
        for each in quitters:
            if each.rank==1:
                if each.gender==0:
                    f_assis_quit+=1
                else:
                    m_assis_quit+=1
            if each.rank==2:
                if each.gender==0:
                    f_asso_quit+=1
                else:
                    m_asso_quit+=1
            if each.rank ==3:
                if each.gender==0:
                    f_full_quit+=1
                else:
                    m_full_quit+=1
            
            self.schedule.remove(each)
        # print("quitters",f_assis_quit,m_assis_quit,f_asso_quit,m_asso_quit,f_full_quit,m_full_quit)
        return quitters 
# -------------------------------------------------------------------------   
    def salary_variance(self):
        female_assistant_income = []
        male_assistant_income = []
        female_associate_income = []
        male_associate_income = []
        female_full_income = []
        male_full_income = []
        
        for each in self.schedule.agents:

            if each.rank == 1:
                
                if each.gender == 0:
                    female_assistant_income.append(each.salary)
                male_assistant_income.append(each.salary)

            if each.rank == 2:
                
                if each.gender == 0:
                    female_associate_income.append(each.salary)
                elif each.gender == 1:
                    male_associate_income.append(each.salary)

            if each.rank == 3:
                
                if each.gender == 0:
                    female_full_income.append(each.salary)
                male_full_income.append(each.salary)

        

       
        
        return np.var(female_assistant_income),\
            np.var(male_assistant_income),\
            np.var(female_associate_income),\
            np.var(male_associate_income),\
            np.var(female_full_income),\
            np.var(male_full_income)
            
    
        
        
 #-------------------------------------------------------------------------------------------------------       
    #calculating number of professors divided by their gender
    def number_of_faculty(self):
        female_assistant = 0
        male_assistant = 0
        female_associate = 0
        male_associate = 0
        female_full = 0
        male_full = 0
        for each in self.schedule.agents:
            if each.rank == 1:
                if each.gender == 0:
                    female_assistant += 1
                else:
                    male_assistant += 1
            if each.rank == 2:
                if each.gender == 0:
                    female_associate += 1
                else:
                    male_associate += 1
            if each.rank == 3:
                if each.gender == 0:
                    female_full += 1
                else:
                    male_full += 1

        
        
        return  female_assistant,\
                male_assistant,\
                female_associate,\
                male_associate,\
                female_full,\
                male_full
                
#---------------------------------------------------------------------------------------------------------------           
    # def the_biggest_differences(self):
    #     female = []
    #     male = []
    #     for each in self.schedule.agents:
    #         if each.gender==0:
    #             female.append(each.salary)
    #         if each.gender==1:
    #             male.append(each.salary)
    #     females_salary  = sum(female)
    #     males_salary  = sum(male)
    #     return abs(males_salary-females_salary),\
    #         males_salary-females_salary
            
#------------------------------------------------------------------------------------------------------------------
    # def compensation(self):           
    #     for each in self.schedule.agents:
    #         if each.gender==0:
    #             each.salary +=10000
        
# ----------------------------------------------------------------------------------------------------
    # def pregnancy(self):
    #     for each in self.schedule.agents:
    #         if each.gender==0 and each.rank==2:
    #             if each.maternal==0:
    #                 if random.random()<.50:
    #                     each.maternal=1
    #                     each.leave = random.randint(1,6)
                          
              
    def steps(self):
        self.schedule.step()
        print("After One Step:")
        self.special_increment(self.num_awards)
        # self.pregnancy()
        promote_ones = self.promotion()
        quitted_ones = self.quitters(self.num_quitters)
        self.hire_new_professors(promote_ones,quitted_ones)

    
              


total_female_assistant_income = []
total_male_assistant_income = []



total_female_assistant_prof = []
total_male_assistant_prof = []



total_female_assistant_increment = []
total_male_assistant_increment = []

#----------------------------------------------

total_female_associate_income  = []
total_male_associate_income = []


total_female_associate_prof = []
total_male_associate_prof = []


total_female_associate_increment =[]
total_male_associate_increment = []

#-----------------------------------------------

total_female_full_prof = []
total_male_full_prof = []

total_female_full_income = []
total_male_full_income = []

total_female_full_increment = []
total_male_full_increment = []
#----------------------------------------------------
female_assistant_salary_variance = []
male_assistant_salary_variance = []
female_associate_salary_variance = []
male_associate_salary_variance = []
female_full_salary_variance =[]
male_full_salary_variance = []


salary_differences = []
actual_salary_differences =[]


# ( percentFemale_assistant,  percentFemale_associate,  percentFemale_full,   hiring_employee_female_percent,  probability_of_promotion_to_the_associate_professor,probability_of_promotion_to_the_full_professor_male
# ,num_awards,num_quitters):
# creating a ProfModel object Second Number is % females
model = ProfModel(.5,.5, .5, .5,1,.6,100,120)
model.creating_agents(500, 300, 200)
for i in range(1000):
    print("Year:", i)
    model.steps()
    income  = model.average_salary_calculation()
    num_faculty = model.number_of_faculty()
    increment = model.average_number_of_increment()
    variance = model.salary_variance()
    # difference = model.the_biggest_differences()
    
    
    total_female_assistant_income.append(income[0])
    total_male_assistant_income.append(income[1])

    total_female_assistant_prof.append(num_faculty[0])
    total_male_assistant_prof.append(num_faculty[1])

    total_female_assistant_increment.append(increment[1])
    total_male_assistant_increment.append(increment[0])

    total_female_associate_income.append(income[3])
    total_male_associate_income.append(income[4])
    
    total_female_associate_prof.append(num_faculty[2])
    total_male_associate_prof.append(num_faculty[3])

    total_female_associate_increment.append(increment[3])
    total_male_associate_increment.append(increment[2])
    
    total_female_full_prof.append(num_faculty[4])
    total_male_full_prof.append(num_faculty[5])

    total_female_full_income.append(income[6])
    total_male_full_income.append(income[7])

    total_female_full_increment.append(increment[5])
    total_male_full_increment.append(increment[4])

    female_assistant_salary_variance.append(variance[0])
    male_assistant_salary_variance.append(variance[1])
    female_associate_salary_variance.append(variance[2])
    male_associate_salary_variance.append(variance[3])
    female_full_salary_variance.append(variance[4])
    male_full_salary_variance.append(variance[5])

    # salary_differences.append(difference[0])
    # actual_salary_differences.append(difference[1])
   
    
    
    
    print("-------------------------------------------------------------------------------")


# # print(salary_differences)
# salary_max = max(salary_differences)
# print(salary_max)
# #just to print the year in which salary difference is the largest
# indexing = salary_differences.index(salary_max)+1
# print(indexing)
# print(actual_salary_differences[indexing-1])
# # ------------------------------------------------------------------------



x = np.arange(len(female_assistant_salary_variance))
width = 0.5
fig, ax = plt.subplots(figsize = (25,2))

rects1 = ax.bar(x - width/2, male_assistant_salary_variance, width, label='Male')
rects2 = ax.bar(x + width/2, female_assistant_salary_variance,
                width, label='Female')
ax.set_ylabel('Variance')
ax.set_xlabel("Year")
ax.set_title("Variance of Assistant Professors' Salary")
ax.legend()
plt.show()


x = np.arange(len(total_female_associate_income))
fig, ax = plt.subplots(figsize=(25, 2))
ax.set_ylim(100000,149000)
ax.set_xlim(-1,1001)
rects1 = ax.bar(x - width/2, total_male_associate_income,
                width, label='Male', linewidth=150)
rects2 = ax.bar(x + width/2, total_female_associate_income,
                width, label='Female', linewidth=150)
ax.set_ylabel('Average Salary of Prof')
ax.set_xlabel("Year")
ax.set_title(
    'Average Annual Salary of Associate Professors by Their Gender Each Year')
ax.legend()
fig.tight_layout()
plt.show()
# -----------



x = np.arange(len(female_associate_salary_variance))
width = 0.5
fig, ax = plt.subplots(figsize = (25,2))

rects1 = ax.bar(x - width/2, male_associate_salary_variance, width, label='Male')
rects2 = ax.bar(x + width/2, female_associate_salary_variance,
                width, label='Female')
ax.set_ylabel('Variance')
ax.set_xlabel("Year")
ax.set_title("Variance of Associate Professors' Salary")
ax.legend()
plt.show()


x = np.arange(len(female_full_salary_variance))
width = 0.5
fig, ax = plt.subplots(figsize = (25,2))

rects1 = ax.bar(x - width/2, male_full_salary_variance, width, label='Male')
rects2 = ax.bar(x + width/2, female_full_salary_variance,
                width, label='Female')
ax.set_ylabel('Variance')
ax.set_xlabel("Year")
ax.set_title("Variance of Full Professor's Salary")
ax.legend()
plt.show()

# -----------------------------------------------------------





# plot of number of assistant and associate professors
x = np.arange(len(total_female_assistant_prof))
width = 0.5  # the width of the bars
fig, ax = plt.subplots(figsize=(25, 2))
rects1 = ax.bar(x - width/2, total_male_assistant_prof, width, label='Male')
rects2 = ax.bar(x + width/2, total_female_assistant_prof,
                width, label='Female')
ax.set_xlim([-1,100])
ax.set_ylabel('Number of Prof')
ax.set_xlabel("Year")
ax.set_title('Number of Assistant Professors by Their Gender Each Year')
ax.legend()
plt.show()

x = np.arange(len(total_female_assistant_prof))
width = 0.5  # the width of the bars
fig, ax = plt.subplots(figsize=(25, 2))
ax.set_xlim(399, 501)
rects1 = ax.bar(x - width/2, total_male_assistant_prof, width, label='Male')
rects2 = ax.bar(x + width/2, total_female_assistant_prof,
                width, label='Female')
ax.set_ylabel('Number of Prof')
ax.set_xlabel("Year")
ax.set_title('Number of Assistant Professors by Their Gender Each Year')
ax.legend()
plt.show()




# for 1000 years of running

x = np.arange(len(total_female_assistant_prof))
width = 0.5  # the width of the bars
fig, ax = plt.subplots(figsize=(25, 2))
ax.set_xlim(-1, 1001)
rects1 = ax.bar(x - width/2, total_male_assistant_prof, width, label='Male')
rects2 = ax.bar(x + width/2, total_female_assistant_prof,
                width, label='Female')
ax.set_ylabel('Number of Prof')
ax.set_xlabel("Year")
ax.set_title('Number of Assistant Professors by Their Gender Each Year')
ax.legend()
plt.show()





# --------------------------------------------------------------------------------------------------

x = np.arange(len(total_female_associate_prof))
width = 0.5  # the width of the bars
fig, ax = plt.subplots(figsize=(25, 2))
ax.set_xlim(-1, 100)
rects1 = ax.bar(x - width/2,total_male_associate_prof , width, label='Male')
rects2 = ax.bar(x + width/2, total_female_associate_prof,
                width, label='Female')
ax.set_ylabel('Number of Prof')
ax.set_xlabel("Year")
ax.set_title('Number of Associate Professors by Their Gender Each Year')
ax.legend()
plt.show()


x = np.arange(len(total_female_associate_prof))
width = 0.5  # the width of the bars
fig, ax = plt.subplots(figsize=(25, 2))
ax.set_xlim(399, 501)
rects1 = ax.bar(x - width/2,total_male_associate_prof , width, label='Male')
rects2 = ax.bar(x + width/2, total_female_associate_prof,
                width, label='Female')
ax.set_ylabel('Number of Prof')
ax.set_xlabel("Year")
ax.set_title('Number of Associate Professors by Their Gender Each Year')
ax.legend()
plt.show()


# for 1000 years

x = np.arange(len(total_female_associate_prof))
width = 0.5  # the width of the bars
fig, ax = plt.subplots(figsize=(25, 2))
ax.set_xlim(-1, 1001)
rects1 = ax.bar(x - width/2,total_male_associate_prof , width, label='Male')
rects2 = ax.bar(x + width/2, total_female_associate_prof,
                width, label='Female')
ax.set_ylabel('Number of Prof')
ax.set_xlabel("Year")
ax.set_title('Number of Associate Professors by Their Gender Each Year')
ax.legend()
plt.show()

# ----------------------------------------------------------------------------------------------
x = np.arange(len(total_female_full_prof))
width = 0.5  # the width of the bars
fig, ax = plt.subplots(figsize=(25, 2))
ax.set_xlim(-1, 100)
rects1 = ax.bar(x - width/2,total_male_full_prof , width, label='Male')
rects2 = ax.bar(x + width/2, total_female_full_prof,
                width, label='Female')
ax.set_ylabel('Number of Prof')
ax.set_xlabel("Year")
ax.set_title('Number of Full Professors by Their Gender Each Year')
ax.legend()
plt.show()



x = np.arange(len(total_female_full_prof))
width = 0.5  # the width of the bars
fig, ax = plt.subplots(figsize=(25, 2))
ax.set_xlim(399, 501)
rects1 = ax.bar(x - width/2,total_male_full_prof , width, label='Male')
rects2 = ax.bar(x + width/2, total_female_full_prof,
                width, label='Female')
ax.set_ylabel('Number of Prof')
ax.set_xlabel("Year")
ax.set_title('Number of Full Professors by Their Gender Each Year')
ax.legend()
plt.show()

# for 1000 years

x = np.arange(len(total_female_full_prof))
width = 0.5  # the width of the bars
fig, ax = plt.subplots(figsize=(25, 2))
ax.set_xlim(-1, 1001)
rects1 = ax.bar(x - width/2,total_male_full_prof , width, label='Male')
rects2 = ax.bar(x + width/2, total_female_full_prof,
                width, label='Female')
ax.set_ylabel('Number of Prof')
ax.set_xlabel("Year")
ax.set_title('Number of Full Professors by Their Gender Each Year')
ax.legend()
plt.show()
# -------------------------------------------------------------------------------------------------------


#plot of income of assistant and associate professors
x = np.arange(len(total_female_assistant_income))
fig, ax = plt.subplots(figsize=(25, 2))
ax.set_ylim(70000,125000)
ax.set_xlim(399,501) 
rects1 = ax.bar(x - width/2, total_male_assistant_income,
                width, label='Male', linewidth=150)
rects2 = ax.bar(x + width/2, total_female_assistant_income,
                width, label='Female', linewidth=150)
ax.set_ylabel('Average Salary of Prof')
ax.set_xlabel("Year")
ax.set_title(
    'Average Annual Salary of Assistant Professors by Their Gender Each Year')
ax.legend()
fig.tight_layout()
plt.show()

# for 1000 years 

#plot of income of assistant and associate professors
x = np.arange(len(total_female_assistant_income))
fig, ax = plt.subplots(figsize=(25, 2))
ax.set_ylim(70000,125000)
ax.set_xlim(-1,1001) 
rects1 = ax.bar(x - width/2, total_male_assistant_income,
                width, label='Male', linewidth=150)
rects2 = ax.bar(x + width/2, total_female_assistant_income,
                width, label='Female', linewidth=150)
ax.set_ylabel('Average Salary of Prof')
ax.set_xlabel("Year")
ax.set_title(
    'Average Annual Salary of Assistant Professors by Their Gender Each Year')
ax.legend()
fig.tight_layout()
plt.show()




# -----------------------------------------------------------------------------------------------------

x = np.arange(len(total_female_associate_income))
fig, ax = plt.subplots(figsize=(25, 2))
ax.set_ylim(70000,139000)
ax.set_xlim(399,501)
rects1 = ax.bar(x - width/2, total_male_associate_income,
                width, label='Male', linewidth=150)
rects2 = ax.bar(x + width/2, total_female_associate_income,
                width, label='Female', linewidth=150)
ax.set_ylabel('Average Salary of Prof')
ax.set_xlabel("Year")
ax.set_title(
    'Average Annual Salary of Associate Professors by Their Gender Each Year')
ax.legend()
fig.tight_layout()
plt.show()




# for 100 years
# --------------------------------------------------------------------------------------------
x = np.arange(len(total_female_full_income))
fig, ax = plt.subplots(figsize=(25, 2))
ax.set_ylim(70000,200000)
ax.set_xlim(399,501)
rects1 = ax.bar(x - width/2, total_male_full_income,
                width, label='Male', linewidth=150)
rects2 = ax.bar(x + width/2, total_female_full_income,
                width, label='Female', linewidth=150)
ax.set_ylabel('Average Salary of Prof')
ax.set_xlabel("Year")
ax.set_title(
    'Average Annual Salary of Full Professors by Their Gender Each Year')
ax.legend()
fig.tight_layout()
plt.show()

# for 1000 years

x = np.arange(len(total_female_full_income))
fig, ax = plt.subplots(figsize=(25, 2))
ax.set_ylim(70000,200000)
ax.set_xlim(-1,1001)
rects1 = ax.bar(x - width/2, total_male_full_income,
                width, label='Male', linewidth=150)
rects2 = ax.bar(x + width/2, total_female_full_income,
                width, label='Female', linewidth=150)
ax.set_ylabel('Average Salary of Prof')
ax.set_xlabel("Year")
ax.set_title(
    'Average Annual Salary of Full Professors by Their Gender Each Year')
ax.legend()
fig.tight_layout()
plt.show()


# ---------------------------------------------------------------------------------------------------------------


#plot of increment of assistant and associate professors


x= np.arange(len(total_female_assistant_increment))
width = 0.5 # the width of the bars
fig, ax = plt.subplots(figsize=(25, 2))
ax.set_xlim(399,501)
rects1 = ax.bar(x - width / 2, total_male_assistant_increment,
                width, label='Male', linewidth=150)
rects2 = ax.bar(x + width / 2, total_female_assistant_increment,
                width, label='Female', linewidth=150)
ax.set_ylabel('Average Increments')
ax.set_title(
    'Average of Assistant Increments by Gender')
ax.set_xlabel("Year")
ax.legend()
fig.tight_layout()
plt.show()

# for 1000 years

x= np.arange(len(total_female_assistant_increment))
width = 0.5 # the width of the bars
fig, ax = plt.subplots(figsize=(25, 2))
ax.set_xlim(-1, 1001)
rects1 = ax.bar(x - width / 2, total_male_assistant_increment,
                width, label='Male', linewidth=150)
rects2 = ax.bar(x + width / 2, total_female_assistant_increment,
                width, label='Female', linewidth=150)
ax.set_ylabel('Average Increments')
ax.set_title(
    'Average of Assistant Increments by Gender')
ax.set_xlabel("Year")
ax.legend()
fig.tight_layout()
plt.show()
# ----------------------------------------------------------------------------------------------------------------------------
x= np.arange(len(total_female_associate_increment))
width = 0.5 # the width of the bars
fig, ax = plt.subplots(figsize=(25, 2))
ax.set_xlim(399,501)
rects1 = ax.bar(x - width / 2, total_male_associate_increment,
                width, label='Male', linewidth=150)
rects2 = ax.bar(x + width / 2, total_female_associate_increment,
                width, label='Female', linewidth=150)
ax.set_ylabel('Average Increments')
ax.set_title(
    'Average of Associate Increments by Gender')
ax.set_xlabel("Year")
ax.legend()
fig.tight_layout()
plt.show()


# for 1000 years

x= np.arange(len(total_female_associate_increment))
width = 0.5 # the width of the bars
fig, ax = plt.subplots(figsize=(25, 2))
ax.set_xlim(-1, 1001)
rects1 = ax.bar(x - width / 2, total_male_associate_increment,
                width, label='Male', linewidth=150)
rects2 = ax.bar(x + width / 2, total_female_associate_increment,
                width, label='Female', linewidth=150)
ax.set_ylabel('Average Increments')
ax.set_title(
    'Average of Associate Increments by Gender')
ax.set_xlabel("Year")
ax.legend()
fig.tight_layout()
plt.show()

# -----------------------------------------------------------------------------------------------------------------

x= np.arange(len(total_female_full_increment))
width = 0.5 # the width of the bars
fig, ax = plt.subplots(figsize=(25, 2))
ax.set_xlim(399,501)
rects1 = ax.bar(x - width / 2, total_male_full_increment,
                width, label='Male', linewidth=150)
rects2 = ax.bar(x + width / 2, total_female_full_increment,
                width, label='Female', linewidth=150)
ax.set_ylabel('Average Increments')
ax.set_title(
    'Average of Full Increments by Gender')
ax.set_xlabel("Year")
ax.legend()
fig.tight_layout()
plt.show()

# for 1000 years


x= np.arange(len(total_female_full_increment))
width = 0.5 # the width of the bars
fig, ax = plt.subplots(figsize=(25, 2))
ax.set_xlim(-1, 1001)
rects1 = ax.bar(x - width / 2, total_male_full_increment,
                width, label='Male', linewidth=150)
rects2 = ax.bar(x + width / 2, total_female_full_increment,
                width, label='Female', linewidth=150)
ax.set_ylabel('Average Increments')
ax.set_title(
    'Average of Full Increments by Gender')
ax.set_xlabel("Year")
ax.legend()
fig.tight_layout()
plt.show()
