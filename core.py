from word_analyzer import WordAnalyzer
from script_analyzer import ScriptAnalyzer
import json


target_video_id = "TLnUJzueBOQ"
cbc_kid = 'SuSTBXGiOsw'
comedy_central = 'fKSiol1uczc'
bbc_news = 'hFAROEKiHl8'

WA = WordAnalyzer()
SA = ScriptAnalyzer()


def analyzeAll(videoId):
    sa_result = json.loads(SA.analyzeScript(videoId))
    wa_result = json.loads(WA.analyzeText(sa_result['script']))

    analyze_result = {}

    analyze_result['videoId'] = sa_result['videoId']
    analyze_result['script'] = sa_result['script']
    analyze_result['avgSyllPerSec'] = sa_result['avgSyllPerSec']
    analyze_result['totalWords'] = wa_result['Total_words']
    analyze_result['avgCEFRScore'] = wa_result['Total_avg_CEFR']
    analyze_result['Readability'] = wa_result['DC_Readability']
    analyze_result['uncommonRatio'] = wa_result['DCL']['uncommon_ratio']

    cefr_sum = [0, 0, 0, 0, 0, 0, 0]
    for checker in ['CEFR', 'Freq']:
        for cefr in ['Oxford', 'Japanese', 'Tv', 'Simpson', 'Gutenberg']:
            if cefr in wa_result[checker]:
                for idx, level in enumerate(['A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'N']):
                    cefr_sum[idx] += len(wa_result[checker]
                                         [cefr]['classified_words'][level])
    cefr_ratio = list(
        map(lambda x: (x/5)/analyze_result['totalWords']*100, cefr_sum))

    analyze_result['A1ratio'] = cefr_ratio[0]
    analyze_result['A2ratio'] = cefr_ratio[1]
    analyze_result['B1ratio'] = cefr_ratio[2]
    analyze_result['B2ratio'] = cefr_ratio[3]
    analyze_result['C1ratio'] = cefr_ratio[4]
    analyze_result['C2ratio'] = cefr_ratio[5]
    analyze_result['Nratio'] = cefr_ratio[6]

    return json.dumps(analyze_result, indent=4)


output = analyzeAll(bbc_news)

with open('bbcnews_test.json', 'wt', encoding='UTF-8') as f:
    f.write(output)
