import re
import unicodedata
import difflib

class PlagiarismDetector:

    def __init__(self):
        self.plagiarism_threshold = 0.5

    def handle_encoding(self, s):
        return str(unicodedata.normalize('NFKD', s).encode('ascii', 'ignore'))

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

        final_ratios = []

        def getKey(item):
            return item[2]

        for i in range(0, len(sigs)):
            sig = sigs[i]

            name1 = sig[0]

            try:
                LL1 = sig[1][1]
            except IndexError:
                LL1 = []

            try:
                LP1 = sig[2][1]
            except IndexError:
                LP1 = []

            try:
                LFN1 = sig[3][1]
            except IndexError:
                LFN1 = []

            for j in range(i, len(sigs)):
                sig2 = sigs[j]

                # for sig2 in sigs:
                name2 = sig2[0]
                try:
                    LL2 = sig2[1][1]
                except IndexError:
                    LL2 = []

                try:
                    LP2 = sig2[2][1]
                except IndexError:
                    LP2 = []

                try:
                    LFN2 = sig2[3][1]
                except IndexError:
                    LFN2 = []

                if name1 == name2:
                    continue

                # print(LL1)
                # print(LL2)


                ratios = []
                if LL1 or LL2:
                    sm = difflib.SequenceMatcher(None, LL1, LL2)
                    # print(sm.ratio())
                    ratios.append(sm.ratio())

                    # if sm.ratio() > ratio:
                    #     #print("Check " + name1 + ": " + sig[1][0])
                    #     #print("VS " + name2 + ": " + sig2[1][0])
                    #     #print("Ratio: " + str(sm.ratio()))
                    #     check = True

                if LP1 or LP2:
                    sm = difflib.SequenceMatcher(None, LP1, LP2)
                    ratios.append(sm.ratio())

                    # if sm.ratio() > ratio:
                    # #     print("Check " + name1 + ": " + sig[2][0])
                    # #     print("VS " + name2 + ": " + sig2[2][0])
                    # #     print("Ratio: " + str(sm.ratio()))
                    #     check = True

                # if LFN1 or LFN2:
                #     sm = difflib.SequenceMatcher(None, LFN1, LFN2)
                #     ratios.append(sm.ratio())
                #     if sm.ratio() > ratio:
                #         # print("Check " + name1 + ": " + sig[3][0])
                #         # print("VS " + name2 + ": " + sig2[3][0])
                #         # print("Ratio: " + str(sm.ratio()))
                #         check = True

                if len(ratios) > 0 and sum(ratios) / len(ratios) > self.plagiarism_threshold:
                    print(name1 + " VS " + name2 + ": " + str(ratios))
                    fr = (ratios[0] + ratios[1]) / 2
                    final_ratios.append([name1, name2, fr])

        for name1, name2, ratio in sorted(final_ratios, key = getKey):
            print(name1 + " VS " + name2 + ": " + str(ratio))
