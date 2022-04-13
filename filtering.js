var product_data = [{
  "id": 90,
  "text": "i shall dm the account number but unsure what you are checking i did eventually get a reduction for arwen but no mention of any days at any time shall as i said send dm difficult to keep track as its been a regular thing of late",
  "date": "2022-02-28"
},
{
  "id": 91,
  "text": "it will probably reduce complaints about power outages as after an hour on hold the battery backup will have gone",
  "date": "2022-02-28"
},
{
  "id": 92,
  "text": "last time it was off for over a week after storm arwen no reduction appeared even after that time elapsed i had to contact you hence this tweet",
  "date": "2022-02-28"
},
{
  "id": 93,
  "text": "records showbased on sms from you that we had an engineer visit on the st th and nd of this month",
  "date": "2022-02-28"
},
{
  "id": 94,
  "text": "i noticed again my bill has not shown any reduction for the tines i had no service",
  "date": "2022-02-28"
},
{
  "id": 95,
  "text": "bt has failed to provide me with a broadband connection since i moved house in november last yearthey now want to charge me a month for a g connection instead totally disgraceful bt is this how you treat customers of years",
  "date": "2022-02-28"
},
{
  "id": 96,
  "text": "i really hate broadband rage advert it stresses me out so much",
  "date": "2022-02-28"
}]

var startDate = new Date("2015-02-28");
var endDate = new Date("2015-03-03");

var resultProductData = product_data.filter(a => {
  var date = new Date(a.date);
  return (date >= startDate && date <= endDate);
});
console.log(resultProductData)