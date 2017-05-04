import re
import unicodedata
import difflib

class PlagiarismDetector:

    def __init__(self):
        self.plagiarism_threshold = 0.7

    def handle_encoding(self, s):
        return str(unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('utf-8', 'replace'))

    def generate_sig(self, d_name, f_name):

        f = open(d_name + '/' + f_name, encoding="utf-8", errors='replace')

        skip_lines = False

        sig = []
        for line in f:
            line = self.handle_encoding(line)

            line = line.split("//")[0]
            line = line.replace("{", "").replace("}", "").replace("?", "")
            line = line.strip()
            if line == "":
                continue

            if line.startswith("System.out.print"):
                continue

            if line.startswith("/*"):
                skip_lines = True
            elif "*/" in line:
                skip_lines = False

            if skip_lines:
                continue

            matches = re.findall('\w+', line)
            if matches is []:
                continue

            #print(line + " " + str(len(matches)))
            sig.append(len(matches))

        f.close()

        return sig

    def compare_sigs(self, sigs):
        # ===================
        # do the comparison of student files

        #This is hardcoded for just two files right now
        #That's the LL and LP
        #TODO: Make this generalize

        ratio_file = open("ratios.txt",'w')

        final_ratios = []

        def getKey(item):
            return item[2]

        for i in range(0, len(sigs)):
            sig1 = sigs[i]

            student_name1 = sig1[0]

            for j in range(i, len(sigs)):
                sig2 = sigs[j]

                # for sig2 in sigs:
                student_name2 = sig2[0]

                if student_name1 == student_name2:
                    continue

                ratios = []
                for sig_num in range(1, len(sig1)):
                    file_sig1_name, file_sig1_sig = sig1[sig_num]

                    try:
                        file_sig2_name, file_sig2_sig = sig2[sig_num]
                    except IndexError:
                        file_sig2_name = None
                        file_sig2_sig = None

                    if file_sig1_sig and file_sig2_sig:
                        sm = difflib.SequenceMatcher(None, file_sig1_sig, file_sig2_sig)
                        # print(sm.ratio())
                        ratios.append(sm.ratio())



                if len(ratios) > 0 and sum(ratios) / len(ratios) > self.plagiarism_threshold:
                    s = student_name1 + " VS " + student_name2 + ": " + str(ratios)
                    print(s)
                    ratio_file.write(s + "\n")
                    final_ratios.append([student_name1, student_name2, sum(ratios) / len(ratios), [ratios]])

        print("Final ratios:")
        for name1, name2, ratio, ratios in sorted(final_ratios, key = getKey):
            s = name1 + " VS " + name2 + ": " + str(ratio) + " " + str(ratios)
            print(s)
            ratio_file.write(s + "\n")

        ratio_file.close()

if __name__ == "__main__":

    PD = PlagiarismDetector()

    sigs = []

    s1 = ["AH"]

    s1.append(["AHCharacter.java", PD.generate_sig("A5", "AHCharacter.java")])

    s2 = ["WO"]
    s2.append(["WOCharacter.java", PD.generate_sig("A5", "WOCharacter.java")])

    sigs = [s1, s2]
    print(sigs)

    PD.compare_sigs(sigs)
