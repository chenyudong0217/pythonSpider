var CryptoJS = require("crypto-js");

function encryption(sourceWord, encryptionKey){
    var key = CryptoJS.enc.Utf8.parse(encryptionKey);
    var iv = CryptoJS.enc.Utf8.parse("5485693214587452");
    var srcs = CryptoJS.enc.Utf8.parse(sourceWord);
    var encrypted = CryptoJS.AES.encrypt(srcs, key, {
        iv: iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7,
    });
    return encrypted.ciphertext.toString();
}

function helloword(){
    return "hello";
}
var password = 'Cyd0217@'
var key = '25597edaee9e4eddb07f2d4d1a09eb49'
console.log(encryption(password, key))