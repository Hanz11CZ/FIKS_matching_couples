# 1.Round: Until there are any free men left, try to connect them with a woman (men=hunters,women=static_gender)
# 2.Round: Now the same from the women's side (men=static_gender,women=hunter) 
#          --- because the 1.round matched based on men's preferences when women had no other choice

class Person():
    def __init__(self,id,preferences,num_of_couples):
        self.id = id
        self.coupled_with = None
        self.used = False
        self.preferences = {}
        # For runtime O(n^2) instead of O(n^3), we should create a dictionary rather than list - for faster access
        for index,other_gender_id in enumerate(preferences):
            self.preferences[other_gender_id] = num_of_couples - index
    
    def is_this_one_better(self,new_partner):
        if self.coupled_with == new_partner:
            return True
        # Compare the sums of:
        #   a) new partner preference of me + my preference of the new partner
        #   b) previous partner preference of me + my preference of the previous partner
        if new_partner.preferences[self.id] + self.preferences[new_partner.id] > self.coupled_with.preferences[self.id] + self.preferences[self.coupled_with.id]:
            return True
        else:
            return False


def createPeopleArraysFromString(arr_of_strings, num_of_couples):
    men = []
    women = []

    for gender in range(0,2): # first go through women, then men

        for person_id in range(0,num_of_couples): # loop through the half of one-gender people
            preferences = []
            current_id = ""
            for i,char in enumerate(arr_of_strings[ (gender*num_of_couples)+person_id ]):
                if char != "," and char != "\n":
                    current_id += char
                    if i+1 == len(arr_of_strings[ (gender*num_of_couples)+person_id ]): # When we reach the end of the whole file
                        preferences.append(int(current_id)-1) # minus 1 for comfortability in working with arrays
                        break
                else:
                    preferences.append(int(current_id)-1)
                    current_id = ""

            this_person = Person(person_id,preferences,num_of_couples)
            if gender == 0:
                women.append(this_person)
            else:
                men.append(this_person)
    
    return(men,women)

def createOutputCouples(men,women):
    men,women = coupleThemUp(men,women,False) # First satisfy men's preferences the best we can --- not much looking at women's needs
    women,men = coupleThemUp(women,men,True) # Second round of women deciding in which couple they wanna be

    resulting_couples = []

    for woman in women:
        resulting_couples.append(str(woman.coupled_with.id+1) + " + " + str(woman.id+1))

    return resulting_couples

# Go through the hunter's preferences of the other gender(static_gender) from the best choice to the worst and:
#   - if the other gender is free, couple them together (looks like an upcoming wedding :))
#   - if the other gender is coupled, see the his/her preferences:   the old hunter X the new hunter -> the one with higher score gets the static_gender
def coupleThemUp(hunting_gender,static_gender,women_turn):
    # Hunters = gender, whose preferences we loop through and try to couple them (hunt the other gender)
    hunting_gender_left = [hunter.id for hunter in hunting_gender]

    # Until there are free hunters, keep coupling:
    i = 0
    while i < len(hunting_gender_left):
        # Try to couple with the best rated person from the other gender and descend
        for static_gender_id in hunting_gender[hunting_gender_left[i]].preferences: 

            # if the person is free couple them up
            if static_gender[static_gender_id].coupled_with == None:
                # When hunting from the women's side, we need to release the previous man with whom the woman was coupled
                if women_turn == True and hunting_gender[hunting_gender_left[i]].coupled_with.coupled_with == hunting_gender[hunting_gender_left[i]]:
                    hunting_gender[hunting_gender_left[i]].coupled_with.coupled_with = None

                hunting_gender[hunting_gender_left[i]].coupled_with = static_gender[static_gender_id]
                static_gender[static_gender_id].coupled_with = hunting_gender[hunting_gender_left[i]]
                break

            # if this new hunter is better rated than the old one by the person:
            elif static_gender[static_gender_id].is_this_one_better(hunting_gender[hunting_gender_left[i]]):

                # If the previous partner was also coupled with this hunted person (if s/he hasn't ran away yet)
                if static_gender[static_gender_id].coupled_with.coupled_with == static_gender[static_gender_id]:
                    old_hunter_on_hold = static_gender[static_gender_id].coupled_with
                    if old_hunter_on_hold.used == True: # If we have already tried this hunter, s/he would remain uncoupled, but if s/he has not tried to couple yet, the turn will get to her/him anyway
                        hunting_gender_left.append(old_hunter_on_hold.id)
                        old_hunter_on_hold.used = False

                # When hunting from the women's side, we need to release the previous man with whom the woman was coupled
                if women_turn == True and hunting_gender[hunting_gender_left[i]].coupled_with.coupled_with == hunting_gender[hunting_gender_left[i]]:
                    hunting_gender[hunting_gender_left[i]].coupled_with.coupled_with = None
                
                hunting_gender[hunting_gender_left[i]].coupled_with = static_gender[static_gender_id]
                static_gender[static_gender_id].coupled_with = hunting_gender[hunting_gender_left[i]]
                break                     

            # this new hunter has no luck, s/he is worse rated...keep hunting
            else:
                continue

        hunting_gender[hunting_gender_left[i]].used = True
        i += 1

    return(hunting_gender,static_gender)

def main(raw_file_name,output_name="RESULTS.txt"):
    f = open(raw_file_name,"r")
    output_f = open(output_name,"w")

    if f and output_f:
        input_lines = f.readlines()
        men,women = createPeopleArraysFromString(input_lines[1:],int(input_lines[0]))
        resulting_couples = createOutputCouples(men,women)

        for couple in resulting_couples: # write to the output file:
            output_f.write(couple+"\n")

    f.close()
    output_f.close()

    return resulting_couples

print( main("input.txt") )