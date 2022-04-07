var startDate = new Date("2015-08-04");
var endDate = new Date("2015-08-12");

var resultProductData = product_data.filter(a => {
  var date = new Date(a.ProductHits);
  return (date >= startDate && date <= endDate);
});
console.log(resultProductData)