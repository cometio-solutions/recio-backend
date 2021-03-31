"""This modules saves data in csv"""
import csv
import random
from recruitment_data import RecruitmentData
from candidate_data import CandidateData

def generate_csv(recruitments_number):
    recruitments = [RecruitmentData() for _ in range(recruitments_number)]
    for recruitment in list(recruitments):
        recruitments.append(RecruitmentData.from_previous_cycle(recruitment))
    with open("recruitments.csv", 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["faculty", "degree", "major_name", "mode",
         "end_date", "cycle_number", "slot_limit"])
        for recruitment in recruitments:
            writer.writerow(list(recruitment))
    candidates = [CandidateData(data) for data in recruitments]
    for recruitment in recruitments:
        number_of_candidates = random.randrange(200)
        for _ in range(number_of_candidates):
            candidate = random.choice(candidates)
            if candidate.can_be_next_recruitment(recruitment):
                candidates.append(CandidateData.from_previous_recruitment(candidate, recruitment))
    with open("candidates.csv", 'w') as csv_file:
        writer = csv.writer(csv_file)
        # writer.writerow(["faculty", "degree", "major_name", "mode",
        #  "end_date", "cycle_number", "slot_limit"])
        for candidate in candidates:
            writer.writerow(list(candidate))


if __name__=='__main__':
    generate_csv(10)
