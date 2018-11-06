
exports.getRndInteger = (min, max) => Math.floor(Math.random() * (max - min) ) + min;

exports.clamp = (number, min, max) => Math.min(Math.max(min, number), max);