#encoding:utf-8
import sys, os
import json
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import src.config.settings as settings
import src.pkulaw.db_func as db_func

baseParam = {"sorts":[{"sort":"IssueDate","sortOrder":"desc"}],"synonym":False,"analyzer":False,"library":"","size":10,"page":1,"group":None,"scopes":[],"moreScopes":[],"searchType":3}

if __name__ == '__main__':
    file = open('params.txt','w')
    index = 0
    params = baseParam
    for key in settings.library:

        params['library'] = settings.library[key]
        if key == '中央法规': EffectivenessDic = settings.zyfg_EffectivenessDic
        elif key == '地方法规': EffectivenessDic = settings.dffg_EffectivenessDic
        #效力阶位
        for effectivenessDic in EffectivenessDic:
            scope_effective = {'analyzer':False,'keyword':effectivenessDic,'scopes':['EffectivenessDic'],'synonym':False,'termType':4}

            #年份
            for year in range(settings.year['begin'], settings.year['end']+1):
                scope_IssueDate = {'analyzer':False,'keyword':str(year),'scopes':['IssueDate'],'synonym':False,'termType':5}

                #时效性
                for TimelinessDic in settings.TimelinessDic:
                    scope_TimelinessDic = {'analyzer':False,'keyword':TimelinessDic,'scopes':['TimelinessDic'],'synonym':False,'termType':4}

                    ## 只有
                    if effectivenessDic.startswith('XE') or effectivenessDic.startswith('XK'):
                        for category in range(settings.Category['begin'],settings.Category['end']+1):
                            if category<10:
                                category = '00'+str(category)
                            elif category<100:
                                category = '0'+str(category)
                            else:
                                category = str(category)
                            scope_Category = {'analyzer':False,'keyword':category,'scopes':['Category'],'synonym':False,'termType':4}
                            scopes = []
                            scopes.append(scope_effective)
                            scopes.append(scope_IssueDate)
                            scopes.append(scope_TimelinessDic)
                            scopes.append(scope_Category)
                            index = index+1
                            params['scopes'] = scopes
                            print(json.dumps(params))

        print(index)