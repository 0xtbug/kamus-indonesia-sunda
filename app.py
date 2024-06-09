from flask import Flask, request, jsonify, render_template
from bst import BST, Word, bst_indonesian, bst_sundanese

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_word', methods=['POST'])
def add_word():
    data = request.json
    indonesian = data['indonesian'].lower()
    sundanese = data['sundanese'].lower()
    
    if bst_indonesian.search(indonesian) or bst_sundanese.search(sundanese):
        return jsonify({"message": "Kata sudah ada"}), 409

    word = Word(indonesian, sundanese)
    bst_indonesian.insert(word, indonesian)
    bst_sundanese.insert(word, sundanese)
    return jsonify({"message": "Kata berhasil ditambahkan"}), 201

@app.route('/delete_word', methods=['DELETE'])
def delete_word():
    data = request.json
    indonesian = data['indonesian'].lower()
    sundanese = data['sundanese'].lower()
    bst_indonesian.delete(indonesian)
    bst_sundanese.delete(sundanese)
    return jsonify({"message": "Kata berhasil dihapus"}), 200

@app.route('/get_translation', methods=['GET'])
def get_translation():
    term = request.args.get('term').lower()
    lang = request.args.get('lang')
    if lang == 'indonesian':
        results = bst_indonesian.search_contains(term)
    else:
        results = bst_sundanese.search_contains(term)

    words_data = [{"indonesian": word.indonesian, "sundanese": word.sundanese} for word in results]
    return jsonify(words_data), 200

@app.route('/get_all_words', methods=['GET'])
def get_all_words():
    words = bst_indonesian.in_order_traversal()
    words_data = [{"indonesian": word.indonesian, "sundanese": word.sundanese} for word in words]
    return jsonify(words_data), 200

if __name__ == '__main__':
    app.run(debug=True)
