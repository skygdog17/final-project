(function () {

	var claus,
		clausImage,
		canvas;

	function loop () {

	  window.requestAnimationFrame(loop);
	  claus.update();
	  claus.render();
	}

	function sprite (options) {

		var that = {},
			frameIndex = 0,
			tickCount = 0,
			ticksPerFrame = options.ticksPerFrame || 0,
			numberOfFrames = options.numberOfFrames || 1;

		that.context = options.context;
		that.width = options.width;
		that.height = options.height;
		that.image = options.image;

		that.update = function () {

            tickCount += 1;

            if (tickCount > ticksPerFrame) {

				tickCount = 0;

                // If the current frame index is in range
                if (frameIndex < numberOfFrames - 1) {
                    // Go to the next frame
                    frameIndex += 1;
                } else {
                    frameIndex = 0;
                }
            }
        };

		that.render = function () {

		  // Clear the canvas
		  that.context.clearRect(0, 0, that.width, that.height);

		  // Draw the animation
		  that.context.drawImage(
		    that.image,
		    frameIndex * that.width / numberOfFrames,
		    0,
		    that.width / numberOfFrames,
		    that.height,
		    0,
		    0,
		    that.width / numberOfFrames,
		    that.height);
		};

		return that;
	}

	// Get canvas
	canvas = document.getElementById("gamecanvas");
	// Create sprite sheet
	clausImage = new Image();

	// Create sprite
	claus = sprite({
		context: canvas.getContext("2d"),
		width: 256,
		height: 256,
		image: clausImage,
		numberOfFrames: 4,
		ticksPerFrame: 7
	});

	// Load sprite sheet
	clausImage.addEventListener("load", loop);
	clausImage.src = "images/claus_right.png";

} ());
