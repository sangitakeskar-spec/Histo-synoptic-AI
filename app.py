import json,datetime,uuid
import pandas as pd
import streamlit as st
from src.checker import assess,CHECKLISTS
st.set_page_config(page_title='HISTO-SYNOPTIC AI | Demo',layout='wide')
st.title('HISTO-SYNOPTIC AI')
st.warning('RESEARCH DEMONSTRATION ONLY — Not validated for clinical use. Synthetic reports only. No automatic sign-out or staging.')
st.caption('AI detects → AI explains → Human verifies → Pathologist approves')
tab1,tab2=st.tabs(['Report QA demo','Synthetic dataset dashboard'])
with tab1:
    a,b=st.columns(2)
    specialty=a.selectbox('Specialty',list(CHECKLISTS))
    procedure=b.selectbox('Procedure',['Resection','Biopsy','Polypectomy','Curettage','Other'])
    st.info('Checklist scope: '+CHECKLISTS[specialty]['scope'])
                     demo_reports = {
            "Breast": """SPECIMEN: Breast resection
Laterality: Left
Histologic type: Invasive ductal carcinoma
Tumor size: 25 mm
Nottingham grade: 2
Margins: Negative
Lymphovascular invasion: Not identified
Regional lymph nodes: 0/12 involved""",

            "CRC": """SPECIMEN: Colon resection
Histologic type: Adenocarcinoma
Tumor size: 35 mm
Tumor grade: Moderately differentiated
Depth of invasion: Muscularis propria
Margins: Negative
Lymphovascular invasion: Not identified
Regional lymph nodes: 0/15 involved""",

            "Lung": """SPECIMEN: Lung resection
Histologic type: Adenocarcinoma
Tumor size: 30 mm
Histologic grade: Moderately differentiated
Margins: Negative
Lymphovascular invasion: Not identified
Regional lymph nodes: 0/10 involved""",

            "Endometrial": """SPECIMEN: Hysterectomy
Histologic type: Endometrioid carcinoma
Tumor size: 30 mm
Histologic grade: FIGO grade 2
Myometrial invasion: Present
Lymphovascular invasion: Not identified
Margins: Negative"""
        }
            if "demo_text" not in st.session_state:
            st.session_state.demo_text = ""

            if st.button("📄 Load Demo Report"):
                st.session_state.demo_text = demo_reports[specialty]

            report = st.text_area(
                "Paste a SYNTHETIC histopathology report",
                key="demo_text",
                height=230,
                placeholder="SPECIMEN: Colon resection..."
                )
    if st.button('Analyze demonstration report',type='primary'):
        if not report.strip():st.error('Paste a synthetic report first.')
        else:
            result=assess(report,specialty,procedure)
            st.session_state['qa']={'report_id':'DEMO-'+uuid.uuid4().hex[:8].upper(),'reviewed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'specialty':specialty,'procedure':procedure,'result':result,'reviewer_actions':{}}
    if 'qa' in st.session_state:
        qa=st.session_state['qa']; r=qa['result']
        if not r['applicable']:st.error(r['reason'])
        else:
            st.metric('Keyword-detection coverage (NOT clinical completeness)',f"{r['completeness_pct']}%",help='Proportion of illustrative elements with at least one matching phrase; can produce false positives and negatives.')
            st.subheader('Elements requiring human review')
            if not r['flags']:st.success('No missing keywords detected. This does NOT establish completeness.')
            for i,flag in enumerate(r['flags']):
                st.write('**'+flag['element']+'** — '+flag['status'])
                st.caption(flag['suggestion'])
                qa['reviewer_actions'][flag['element']]=st.selectbox('Reviewer decision — '+flag['element'],['Pending','Confirm omission','Present elsewhere','Not applicable','Escalate'],key=f"{qa['report_id']}-{i}")
            with st.expander('Potentially present fields — verification required'):
                st.dataframe(pd.DataFrame(r['present_elements']),use_container_width=True)
        st.download_button('Download audit JSON',json.dumps(qa,indent=2),file_name=f"{qa['report_id']}.json",mime='application/json')
with tab2:
    df=pd.read_csv('data/synthetic_reports.csv')
    st.metric('Synthetic cases',len(df))
    st.bar_chart(df.groupby('specialty').size())
    st.bar_chart(df.groupby('specialty')['generator_omission_count'].mean())
    st.caption('Generator-derived omissions are not independent gold-standard labels. No clinical performance claims.')
