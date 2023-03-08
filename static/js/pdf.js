

function downloadText() {
  var content = document.getElementById("downloadPDF").innerText;
  var blob = new Blob([content], { type: "text/plain" });
  var url = URL.createObjectURL(blob);
  var a = document.createElement("a");
  
  a.href = url;
  a.download = "Patient-Summary.txt";
  document.body.appendChild(a);
  a.click();
  
  setTimeout(function() {
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  }, 0);
}

function downloadPDF() {
  var doc = new jsPDF();
  var content = document.getElementById("downloadPDF");

  doc.fromHTML(content, -1, -1);
  doc.save("my-content.pdf");
}

function generatePDF() {
  const element = document.getElementById("downloadPDF");
  const opt = {
    margin: 1,
    filename: "Patient-Summries.pdf",
    image: { type: "jpeg", quality: 0.98 },
    html2canvas: { scale: 2 },
    pagebreak: { mode: ["css", "legacy"] },
    jsPDF: { unit: "in", format: "letter", orientation: "portrait" },
  };
  console.log(element);
  html2pdf().from(element).set(opt).save();
}

function copyTag(elementId) {
  const element = document.getElementById(elementId);
  const text = element.innerHTML;
  navigator.clipboard.writeText(text.replace(/<[^>]*>/g, ""));

  document.getElementById("copy-button").setAttribute("title", "copied");
  document.getElementById("copy-button").innerHTML = "copied";
}

function loadder() {
  $(document).ready(function(event) {
    var form = document.getElementById("patientFormId");

    if (form.checkValidity() === false) {
      event.preventDefault();
      event.stopPropagation();
    } else {
    $('#loader').show();
    $('#hidden-logo').hide();
    $('#invoice').hide();
    $('#hide-button').hide();
    }
    
  });

  $(window).on('load', function() {
    $('#loader').hide();
  });
}
