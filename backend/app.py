from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

expenses = []

@app.route('/api/expenses', methods=['POST'])
def add_expense():
    data = request.json
    shares = data.get('shares', [])
    expense = {
        'id': len(expenses),
        'description': data.get('description'),
        'amount': data.get('amount'),
        'shares': shares
    }
    expenses.append(expense)
    return jsonify(expense), 201

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    return jsonify(expenses)

@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    global expenses
    expenses = [exp for exp in expenses if exp['id'] != expense_id]
    return jsonify({'message': 'Expense deleted successfully'}), 200

@app.route('/api/expenses/<int:expense_id>/pay', methods=['PUT'])
def mark_paid(expense_id):
    data = request.json
    person = data.get('person')
    paid_status = data.get('paid', False)

    for expense in expenses:
        if expense['id'] == expense_id:
            for share in expense['shares']:
                if share['person'] == person:
                    share['paid'] = paid_status
                    break
            break
    return jsonify({'message': 'Payment status updated'}), 200

if __name__ == '__main__':
    app.run(debug=True)
