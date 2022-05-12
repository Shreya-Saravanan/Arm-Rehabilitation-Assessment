// Live Recording

  // Store a reference of the preview video element and a global reference to the recorder instance
  var video = document.getElementById('my-preview');
  let counterUI = document.getElementById("start-counter");
  let durationID;
  var recorder;
  var runtime;
  var Webpage = "{{ Exercise.Exercise_Webpage }}";
  console.log(Webpage);

  var Exercise_Name = "{{ Exercise.Exercise_Title }}";
  console.log(Exercise_Name);

  var Exercise_Model = "{{ Exercise.Exercise_Models }}";
  console.log(Exercise_Model);

  var upload_blob = null;
  var upload_filename = '';

  function convertTime(seconds) {
    runtime = seconds;

    var sec_num = parseInt(seconds); // don't forget the second param

    var hours = Math.floor(sec_num / 3600);
    var minutes = Math.floor((sec_num - (hours * 3600)) / 60);

    var seconds = sec_num - (hours * 3600) - (minutes * 60);
    console.log(minutes, seconds);

    if (minutes < 10) { minutes = "0" + minutes; }
    if (seconds < 10) { seconds = "0" + seconds; }

    return minutes + ':' + seconds;
  };

  function startRecording() {
    // Disable start recording button
    // Request access to the media devices
    navigator.mediaDevices.getUserMedia({
      audio: false,
      video: true
    }).then(function (stream) {
      // Display a live preview on the video element of the page
      setSrcObject(stream, video);
      var seconds = 0
      durationID = setInterval(() => {
        counterUI.innerHTML = convertTime(seconds)
        seconds++
      }, 1000);
      // Start to display the preview on the video element
      // and mute the video to disable the echo issue !
      video.play();
      video.muted = true;
      // Initialize the recorder
      recorder = new RecordRTCPromisesHandler(stream, {
        mimeType: 'video/webm',
        bitsPerSecond: 128000
      });
      // Start recording the video
      recorder.startRecording().then(function () {
        console.info('Recording video ...');
      }).catch(function (error) {
        console.error('Cannot start video recording: ', error);
      });
      // release stream on stopRecording
      recorder.stream = stream;
      // Enable stop recording button
      document.getElementById('btn-stop-recording').disabled = false;
    }).catch(function (error) {
      console.error("Cannot access media devices: ", error);
    });
  }


  // Download Blob Function
  function downloadBlob(blob = upload_blob, name = upload_filename) {

    // Convert blob into a Blob URL (URL pointing to an object in the browser's memory)
    const blobUrl = URL.createObjectURL(blob);

    // Create a link element
    const download_link = document.createElement("a");

    // Set link's href to point to the Blob URL
    download_link.href = blobUrl;
    download_link.download = ((new Date()).toISOString()) + '_upload_recording_' + runtime + '.mp4';;

    // Append link to the body
    document.body.appendChild(download_link);

    // Dispatch click event on the link
    // This is necessary as link.click() does not work on the latest firefox
    download_link.dispatchEvent(
      new MouseEvent('click', {
        bubbles: true,
        cancelable: true,
        view: window
      })
    );

    // Remove link from body
    document.body.removeChild(download_link);
  }

  // When the user clicks on start video recording
  function startTimer(evt) {
    // console.log(evt);
    evt.preventDefault();
    document.getElementById("btn-start-recording").disabled = true
    let counter = 2;
    let intervalID = setInterval(() => {
      if (counter == -1) {
        counterUI.innerHTML = "";
        clearInterval(intervalID);
        startRecording();
        return;
      }
      counterUI.innerHTML = counter;
      counter--;
    }, 1000);
    return false;
  }
  // When the user clicks on Stop video recording
  document.getElementById('btn-stop-recording').addEventListener("click", function () {
    this.disabled = true;
    clearInterval(durationID)
    counterUI.innerHTML = ''
    recorder.stopRecording().then(async function () {
      console.info('stopRecording success');

      if (recorder.blob) {
        var blob = URL.createObjectURL(recorder.blob);
        console.log(blob);

        var fileType = 'video';
        var fileName = ((new Date()).toISOString()) + '_live_recording_' + runtime + '.mp4';

        upload_blob = recorder.blob;
        upload_filename = fileName;

        var formData = new FormData();
        var boundary = String(Math.random()).slice(2);

        formData.append("event_id", window.event_id);
        formData.append("type", recorder.type);
        formData.append("upload_option", "option");
        formData.append('file', recorder.blob, fileName);
        formData.append('Model', Exercise_Model);
        formData.append('Webpage', Webpage);
        formData.append('Exercise_Name', Exercise_Name);


        console.log('Before POST Request')
        try {
          let res = await axios.post('/Exercise/{{ Exercise["Exercise_Webpage"] }}', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          });
          document.body.innerHTML = res.data;
          console.log(res.data);
          console.log(res);

        } catch (error) {
          console.log(error);
        }
      }

      //video.play();
      // Unmute video on preview
      //video.muted = true;

      // Stop Device Streaming
      recorder.stream.stop();

      // Enable Start-Recording Button again !
      document.getElementById('btn-start-recording').disabled = false;

      // Enable download button
      document.getElementById('btn-download').disabled = false;

    }).catch(function (error) {
      console.error('stopRecording failure', error);
    });
  }, false);

  function sendToServer(blob) {
  }
