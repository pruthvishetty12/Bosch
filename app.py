from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd

app = Flask(__name__)
app.secret_key = 'Bosch.com'

# User data
users = {
    'Manjunath': 'Secure@998811',
    'Harshith': 'Secure@998811',
    'Nithin': 'Secure@998811',
    'Naveen': 'Secure@998811',
    'Suhas': 'Secure@998811'
}

@app.route('/', methods=['GET', 'POST'])
def login():
    error1 = None
    if request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']
        error1 = None
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('user'))
        else:
            error1=f'Invalid username or password!'
    
    return render_template('login.html',error1=error1)

@app.route('/user', methods=['GET', 'POST'])
def user():
    if 'username' in session:
        username = session['username']
        error = None
        msg = None
        sap_value = None
        ll_value = None
        main_part_number = ''
        sub_part_number = ''
        
        if request.method == 'POST':
            main_part_number = request.form['main_part_number'].strip()
            sub_part_number = request.form['sub_part_number'].strip()
            
            try:
                excel_file = 'LOADING LIST SMT.xlsx'
                excel_data = pd.read_excel(excel_file, sheet_name=None)
                
                if main_part_number in excel_data:
                    df = excel_data[main_part_number]
                    
                    if 'PART NUMBERS' in df.columns:
                        df['PART NUMBERS'] = df['PART NUMBERS'].astype(str).str.strip()
                        
                        if sub_part_number in df['PART NUMBERS'].values:
                            row = df[df['PART NUMBERS'] == sub_part_number].iloc[0]
                            sap_value = row.get('SAP', 0)
                            ll_value = row.get('LL', 0)

                            if pd.isna(sap_value):
                                sap_value = 0
                            if pd.isna(ll_value):
                                ll_value = 0
                            msg = f"{sap_value} SAP and {int(ll_value)} LL mounted Successfully"
                        else:
                            error = f"Make sure that Main Part Number {main_part_number} and Sub Part Number {sub_part_number} are correct."
                    else:
                        error = f"'PART NUMBERS' column not found in {main_part_number}."
                else:
                    error = f"Main part number {main_part_number} not found."
                
            except Exception as e:
                error = f"Error processing Excel file: {str(e)}"
        
        return render_template('user.html', username=username, error=error, msg=msg,
                               main_part_number=main_part_number, sub_part_number=sub_part_number)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
