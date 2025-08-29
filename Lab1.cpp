/*  lexical analyzer code  */
#include <bits/stdc++.h>
using namespace std;

unordered_set<string> keywords = {
    "int", "float", "void", "main", "include", "return"
};

unordered_set<string> operators = {
    "+", "=", "%"
};

unordered_set<string> symbols = {
    "[", "]", "{", "}", "(", ")", ";", ".", "#"
};

bool isNumber(const string& token){
    bool decimalPoint = false;
    for(char ch : token){
        if(ch == '.'){
            if(decimalPoint) return false;
            decimalPoint = true;
        } else if(!isdigit(ch)){
            return false;
        }
    }
    return !token.empty();
}

void classifytoken(const string& token){
    if(token.empty()) return;

    if(keywords.find(token) != keywords.end()){
        cout << token << " --> keyword\n";
    }
    else if(operators.find(token) != operators.end()){
        cout << token << " --> operator\n";
    }
    else if(symbols.find(token) != symbols.end()){
        cout << token << " --> symbol\n";
    }
    else if(isNumber(token)){
        cout << token << " --> number\n";
    }
    else{
        cout << token << " --> identifier\n";
    }
}

vector<string> tokenize(const string& line){
    vector<string> tokens;
    string token;
    for(char ch : line){
        if(isspace(ch)){
            if(!token.empty()){
                tokens.push_back(token);
                token.clear();
            }
        }
        else if(operators.count(string(1, ch)) || symbols.count(string(1, ch))){
            if(!token.empty()){
                tokens.push_back(token);
                token.clear();
            }
            tokens.push_back(string(1, ch));
        }
        else{
            token += ch;
        }
    }
    if(!token.empty()) tokens.push_back(token);
    return tokens;
}

int main(){
    ifstream infile("input.txt");
    if(!infile){
        cerr << "Error opening file!\n";
        return 1;
    }
    
    string line;
    while(getline(infile, line)){
        vector<string> tokens = tokenize(line);
        for(const string& tok : tokens){
            classifytoken(tok);
        }
    }

    infile.close();
    return 0;
}



/* 
INPUT for CODE.

#include <iostream>
int main() {
float value = 10.5;
int count = 100;
return count;
}

*/