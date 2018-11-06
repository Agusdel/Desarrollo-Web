var GameObject = require('./gameobject.js');
var module = require('module');
const Engine = require('./engine.js');

module.exports = class Ball extends GameObject {

    constructor(name, context, sprite, sizeX, sizeY, backgroundWidth, backgroundHeight) {
        // Chain constructor with super
        super(name, context, sprite, sizeX, sizeY, backgroundWidth, backgroundHeight);

        this.verticalVelocity = 0;
        this.horizontalVelocity = 0;

	    this.minHorizontalVelocity = 0.3;
	    this.maxHorizontalVelocity = 0.7;
	    this.minBounceForce = 10;
	    this.maxBounceForce = 40;
    }

    start()
    {
    	super.start();

		this.horizontalVelocity = Engine.getRndInteger(this.minHorizontalVelocity, this.maxHorizontalVelocity) * ((Engine.getRndInteger(0,1) == 1) ? 1 : -1);
		setPosition(this.backgroudWidth * 0.25, Math.floor(this.backgroundHeight/10));
    }

    update(deltaTime)
    {
    	super.update();

    	if (!isGameOver)
    	{
			updateMovement(deltaTime);
		}
    }

    updateMovement(deltaTime)
    {
    	this.verticalVelocity += gravity * deltaTime;

    	move(this.horizontalVelocity * deltaTime, this.verticalVelocity);

    	if (this.y >= groundY - this.sizeY)
    	{
    		setPosition(this.x, groundY - this.sizeY);
    		var bounceForce = Engine.getRndInteger(this.minBounceForce,this.maxBounceForce);
    		this.verticalVelocity = -bounceForce;
    	}
    	else if (this.y <= 0)
    	{
    		setPosition(this.x, 0);
    		this.verticalVelocity *= -1;
    	}

    	if (this.x >= this.backgroudWidth - this.sizeX)
    	{
    		setPosition(this.backgroudWidth - this.sizeX, this.y);
    		this.horizontalVelocity = Engine.getRndInteger(this.minHorizontalVelocity, this.maxHorizontalVelocity) * -1;
    	}
    	else if (this.x <= 0)
    	{
    		setPosition(0, this.y);
    		this.horizontalVelocity = Engine.getRndInteger(this.minHorizontalVelocity, this.maxHorizontalVelocity);
    	}

    }
}