var module = require('module');

module.exports = class GameObject {

    constructor(name, context, sprite, sizeX, sizeY, backgroundWidth, backgroundHeight) {
        this.name = name;
        this.context = context;
        this.backgroundWidth = backgroundWidth;
        this.backgroundHeight = backgroundHeight;
        this.sprite = sprite;
        this.x = 0;
        this.y = 0;
        this.sizeX = sizeX;
        this.sizeY = sizeY;
    }

    start() {}

    internalUpdate()
    {
    	clear();
    	update();
    	draw();
    }

    update(deltaTime){}

    move(x, y)
    {
    	context.translate(x,y);
        this.x += x;
        this.y += y;
    }

    setPosition(x, y)
    {
        context.translate(x - this.x, y - this.y);
        this.x = x;
        this.y = y;
    }

    draw()
    {
    	context.drawImage(this.sprite, 0, 0, this.sizeX, this.sizeY);
    }

    clear()
    {
    	context.clearRect(0, 0, this.sizeX, this.sizeY);
    }
}