// window.onload = function() {
//     document.getElementById('dowloadPDF').addEventListener('click', ()=> {
//         const invoice = tis.getElementById('invoice');
//         console.log(invoice);
//         console.log(window);
//         var opt = {
//             margin: 1,
//             filename: 'Patient-Summries.pdf',
//             image: { type: 'jpeg', quality: 0.98 },
//             html2canvas: { scale: 2 },
//             jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
//         };
//         html2pdf().from(invoice).set(opt).save();
//     })
// }

function generatePDF() {
  const element = document.getElementById("invoice");
  // add properties
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
