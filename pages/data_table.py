import streamlit as st
import numpy as np
import pandas as pd
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder, JsCode

def app():
    # user = st.session_state["username"]
    st.title('Update budget & estimate')
    user_projecten = ['NL, Westparkwest - GWL', 'Voorbeeldproject']
    user_projecten_selectie = ['--'] + user_projecten
    project_selector = st.sidebar.selectbox('Selecteer project', user_projecten_selectie)
    st.session_state['Project'] = project_selector
    if project_selector == '--':
        st.write('Selecteer een project om budget & estimate weer te geven')
    else:
        # Fill a dataframe and cache it
        @st.cache(allow_output_mutation=True)
        def get_dataframe(project_name:str='NL, Westparkwest - GWL'):
            if project_name == 'NL, Westparkwest - GWL':
                file = "/Users/eefje/python_projects/stijn/data/test eef.xlsx"
                excel = pd.read_excel(file, sheet_name="Blad3", dtype=str, skiprows = 2)
                excel = excel.iloc[7: , :]
                excel['WBS-type'] = excel['Id'].str[-2:]
                # Drop rows where
                excel = excel[excel['WBS-type']!="00"]
                excel = excel[['WBS', 'Latest approved budget', 'Estimate to Complete']]
                for col in ['Latest approved budget', 'Estimate to Complete']:
                    excel[col] = excel[col].astype(float).apply(lambda x: round(x, 2))
                excel.rename(columns={'Latest approved budget':'Budget', 'Estimate to Complete':'Estimate'}, inplace=True)
            else:
                excel = pd.DataFrame()
            return excel.reset_index(drop=True)

        df = get_dataframe(project_selector).reset_index(drop=True)

        if len(df)>0:
            # Build customized table
            gb = GridOptionsBuilder.from_dataframe(df)
            # make columns editable
            gb.configure_columns(['Budget', 'Estimate'], editable=True)

            js = JsCode("""
                function(e) {
                    let api = e.api;
                    let rowIndex = e.rowIndex;
                    let col = e.column.colId;
                    
                    let rowNode = api.getDisplayedRowAtIndex(rowIndex);
                    api.flashCells({
                      rowNodes: [rowNode],
                      columns: [col],
                      flashDelay: 10000000000
                    });
                };
                """)

            gb.configure_grid_options(onCellValueChanged=js)
            gb.configure_grid_options(domLayout='autoHeight')
            go = gb.build()

            ag = AgGrid(df, gridOptions=go,  key='grid2', allow_unsafe_jscode=True, reload_data=False, fit_columns_on_grid_load= True)

            new_df = ag['data'].reset_index(drop=True)

            # Grafiek met estimate to complete = budget - obligo's - handmatige wijzigigen

            submit_data_edits = st.button('Bevestig aanpassingen')
            if submit_data_edits:
                st.write('Check of je aanpassingen goed zijn doorgevoerd')
                new_df = new_df.add_suffix(' - new').copy()
                edits = pd.concat([new_df, df], axis=1)
                for col in ['Budget', 'Estimate']:
                    edits['Delta'] = (edits[f'{col} - new'] - edits[f'{col}']).astype(float)
                    edits[f'{col} - new'] = edits[f'{col} - new'].astype(float)
                    edits_sub = edits[['WBS', col, f'{col} - new', 'Delta']]
                    edits_sub = edits_sub[abs(edits_sub['Delta'])>0].reset_index(drop=True)
                    if len(edits_sub)>0:
                        gb = GridOptionsBuilder.from_dataframe(edits_sub)
                        threshold_delta=10000
                        cellstyle_jscode = JsCode(
                            """
                        function(params) {
                            if (Math.abs(params.value) > """+str(threshold_delta)+""") {
                                return {
                                    'color': 'black',
                                    'backgroundColor': 'lightblue'
                                }
                            } else {
                                return {
                                    'color': 'black',
                                    'backgroundColor': 'white'
                                }
                            }
                        };
                        """
                        )

                        gb.configure_column("Delta", cellStyle=cellstyle_jscode)
                        gb.configure_grid_options(domLayout='autoHeight')
                        go = gb.build()
                        grid = AgGrid(edits_sub, enable_enterprise_modules=True, update_mode=GridUpdateMode.SELECTION_CHANGED, gridOptions=go, allow_unsafe_jscode=True, key=f'grid_{col}', fit_columns_on_grid_load= True, editable=False)
                        edits_sub['AbsDelta'] = abs(edits_sub['Delta'])
                        if edits_sub.AbsDelta.max()>threshold_delta:
                            st.write(f'Let op: je hebt verschillen aangebracht in een {col} onderdeel van meer dan {threshold_delta} euro.')

                submit_data_edits_check = st.button('Verzend aanpassingen')
                if submit_data_edits_check:
                    st.write('Update verzonden')




