var calendar = new FullCalendar.Calendar(document.getElementById("calendar"), {
      contentHeight: 'auto',
      aspectRatio: 0.2,
      initialView: "dayGridMonth",
      headerToolbar: {
        start: 'title', // will normally be on the left. if RTL, will be on the right
        center: 'legend',
        end: 'today prev,next' // will normally be on the right. if RTL, will be on the left
      },
      customButtons: {
        legend: {
          text: '' // We'll use this space to insert our legend HTML
        }
      },
      selectable: true,
      editable: true,
      initialDate: '2024-04-23',
      events: [
        {
          title: 'Creatures of the Night Spotlight Tour',
          start: '2024-05-25',
          end: '2024-05-25',
          className: 'bg-gradient-success',
          category: 'conservation',
          url: 'https://www.eventbrite.com.au/e/creatures-of-the-night-spotlight-tour-tickets-880016431837?aff=ebdssbdestsearch'
        },
        {
          title: 'Simon Kirby - How humans got language: learning, culture & evolution',
          start: '2024-06-17',
          end: '2024-06-17',
          className: 'bg-gradient-success',
          category: 'conservation',
          url: 'https://www.eventbrite.com.au/e/simon-kirby-how-humans-got-language-learning-culture-evolution-tickets-871434232247?aff=ebdssbdestsearch'
        },
        {
          title: 'Eucalypts of Bellbird Dell',
          start: '2024-05-25',
          end: '2024-05-25',
          className: 'bg-gradient-success',
          category: 'conservation',
          url: 'https://www.eventbrite.com.au/e/eucalypts-of-bellbird-dell-tickets-879202196437?aff=ebdssbdestsearch'  
        },
        {
          title: 'Drawing conversations from classical to AI',
          start: '2024-05-25',
          end: '2024-05-25',
          className: 'bg-gradient-danger',
          category: 'wildlife',
          url: 'https://www.eventbrite.com.au/e/drawing-conversations-from-classical-to-ai-tickets-886528860687?aff=ebdssbdestsearch'
        },
        {
          title: 'Birds of Hume talk and walk',
          start: '2024-07-03',
          end: '2024-07-03',
          className: 'bg-gradient-danger',
          category: 'wildlife',
          url: 'https://www.eventbrite.com.au/e/birds-of-hume-talk-and-walk-tickets-877005817007?aff=ebdssbdestsearch' 
        },
        {
          title: 'An evening with Caroline Pope- Animal Communicator @ Pakenham Library',
          start: '2024-05-10',
          end: '2024-05-10',
          className: 'bg-gradient-danger',
          category: 'wildlife',
          url: 'https://www.eventbrite.com.au/e/an-evening-with-caroline-pope-animal-communicator-pakenham-library-tickets-774141517117?aff=ebdssbdestsearch'
        },
        {
          title: 'Bridgewater Lake Wildlife Habitat Garden',
          start: '2024-06-18',
          end: '2024-06-18',
          className: 'bg-gradient-danger',
          category: 'wildlife',
          url: 'https://www.eventbrite.com.au/e/bridgewater-lake-wildlife-habitat-garden-tickets-877693754647?aff=ebdssbdestsearch'
        },
        {
          title: 'Bird Walk in Yarran Dheran',
          start: '2024-05-05',
          end: '2024-05-05',
          className: 'bg-gradient-danger',
          category: 'wildlife',
          url: 'https://www.eventbrite.com.au/e/bird-walk-in-yarran-dheran-tickets-877091102097?aff=ebdssbdestsearch'  
        },
        {
          title: 'Fungi Guided Walk with Dr Sapphire McMullan-Fisher',
          start: '2024-05-25',
          end: '2024-05-25',
          className: 'bg-gradient-success',
          category: 'conservation',
          url: 'https://www.eventbrite.com.au/e/fungi-guided-walk-with-dr-sapphire-mcmullan-fisher-tickets-867081422877?aff=ebdssbdestsearch'
        },
        {
          title: 'Yarra Valley EcoVineyards ground covers seminar and hydroseeding demo',
          start: '2024-05-13',
          end: '2024-05-13',
          className: 'bg-gradient-danger',
          category: 'wildlife',
          url: 'https://www.eventbrite.com.au/e/yarra-valley-ecovineyards-ground-covers-seminar-and-hydroseeding-demo-tickets-865223174807?aff=ebdssbdestsearch'
        },
        {
          title: 'Koala Conservation Day: Weeding and Wildlife Walk',
          start: '2024-05-04',
          end: '2024-05-04',
          className: 'bg-gradient-danger',
          category: 'wildlife',
          url: 'https://www.eventbrite.com.au/e/koala-conservation-day-weeding-and-wildlife-walk-tickets-712808016967?aff=ebdssbdestsearch'
        },
        {
          title: 'Mornington Peninsula EcoVineyards ground covers seminar & hydroseeding demo',
          start: '2024-05-15',
          end: '2024-05-15',
          className: 'bg-gradient-success',
          category: 'conservation',
          url: 'https://www.eventbrite.com.au/e/mornington-peninsula-ecovineyards-ground-covers-seminar-hydroseeding-demo-tickets-865240426407?aff=ebdssbdestsearch'
        },
        {
          title: '3 Day Frame Drum Making Intensive',
          start: '2024-06-14',
          end: '2024-06-14',
          className: 'bg-gradient-danger',
          category: 'wildlife',
          url: 'https://www.eventbrite.com.au/e/3-day-frame-drum-making-intensive-tickets-718314637417?aff=ebdssbdestsearch'
        },
        {
          title: 'Architectural Glass with Bruce Hutton',
          start: '2024-05-03',
          end: '2024-05-03',
          className: 'bg-gradient-success',
          category: 'conservation',
          url: 'https://www.eventbrite.com.au/e/architectural-glass-with-bruce-hutton-tickets-829804175627?aff=ebdssbdestsearch'
        },
        {
          title: 'City Nature Challenge 2024 bird & flora bushwalk at Mt Ridley NCR',
          start: '2024-05-04',
          end: '2024-05-04',
          className: 'bg-gradient-success',
          category: 'conservation',
          url: 'https://www.eventbrite.com.au/e/city-nature-challenge-2024-bird-flora-bushwalk-at-mt-ridley-ncr-tickets-827945245517?aff=ebdssbdestsearch'
        },
        
        {
          title: 'Eastern Long-necked Turtles at Yarran Dheran',
          start: '2024-05-31',
          end: '2024-05-31',
          className: 'bg-gradient-success',
          category: 'conservation',
          url: 'https://www.eventbrite.com.au/e/eastern-long-necked-turtles-at-yarran-dheran-tickets-883054187847?aff=ebdssbdestsearch'
        },
        {
          title: 'Heritage walk of Newport Lakes',
          start: '2024-05-05',
          end: '2024-05-05',
          className: 'bg-gradient-success',
          category: 'conservation',
          url: 'https://www.eventbrite.com.au/e/heritage-walk-of-newport-lakes-tickets-817611035617?aff=ebdssbdestsearch'
        },
        {
          title: 'Biodiversity Blitz @ Bellbird Dell',
          start: '2024-05-05',
          end: '2024-05-05',
          className: 'bg-gradient-success',
          category: 'conservation',
          url: 'https://www.eventbrite.com.au/e/biodiversity-blitz-bellbird-dell-tickets-870811840657?aff=ebdssbdestsearch'
        },
        
        {
          title: 'Australian Heritage Festival - Significant Trees of Rippon Lea',
          start: '2024-05-03',
          end: '2024-05-03',
          className: 'bg-gradient-success',
          category: 'conservation',
          url: 'https://www.eventbrite.com.au/e/australian-heritage-festival-significant-trees-of-rippon-lea-tickets-808530996977?aff=ebdssbdestsearch'
        },
        {
          title: 'Cleopatras Bling presents Usta - Melbourne Design Week',
          start: '2024-05-23',
          end: '2024-05-23',
          className: 'bg-gradient-danger',
          category: 'wildlife',
          url: 'https://www.eventbrite.com.au/e/cleopatras-bling-presents-usta-melbourne-design-week-tickets-861863515977?aff=ebdssbdestsearch'
        },
        {
          title: 'Learn About Citizen Science - how to get involved in a BioBlitz',
          start: '2024-05-05',
          end: '2024-05-05',
          className: 'bg-gradient-success',
          category: 'conservation',
          url: 'https://www.eventbrite.com.au/e/learn-about-citizen-science-how-to-get-involved-in-a-bioblitz-tickets-868150149467?aff=ebdssbdestsearch'
        },
        {
          title: 'Aussie Bush Illustration with Jess Racklyeft',
          start: '2024-06-15',
          end: '2024-06-15',
          className: 'bg-gradient-success',
          category: 'conservation',
          url: 'https://www.eventbrite.com.au/e/aussie-bush-illustration-with-jess-racklyeft-tickets-849137271437?aff=ebdssbdestsearch'
        },
        {
          title: 'City Nature Challenge 2024 guided bushwalk into Wanginu Park, Sunbury',
          start: '2024-05-03',
          end: '2024-05-03',
          className: 'bg-gradient-danger',
          category: 'wildlife',
          url: 'https://www.eventbrite.com.au/e/city-nature-challenge-2024-guided-bushwalk-into-wanginu-park-sunbury-tickets-827948555417?aff=ebdssbdestsearch'
        },
        {
          title: 'City Nature Challenge 2024 Bushtucker walk and talk at Westmeadows',
          start: '2024-05-05',
          end: '2024-05-05',
          className: 'bg-gradient-success',
          category: 'conservation',
          url: 'https://www.eventbrite.com.au/e/city-nature-challenge-2024-bushtucker-walk-and-talk-at-westmeadows-tickets-827942958677?aff=ebdssbdestsearch'
        },
        {
          title: 'Greenvale School Holidays Planting',
          start: '2024-07-08',
          end: '2024-07-08',
          className: 'bg-gradient-danger',
          category: 'wildlife',
          url: 'https://www.eventbrite.com.au/e/greenvale-school-holidays-planting-tickets-877783884227?aff=ebdssbdestsearch'
        },
        {
          title: 'HCG Wicking Beds Workshop',
          start: '2024-05-19',
          end: '2024-05-19',
          className: 'bg-gradient-success',
          category: 'conservation',
          url: 'https://www.eventbrite.com/e/hcg-wicking-beds-workshop-tickets-881632595827?aff=ebdssbdestsearch'      
        },
        {
          title: 'A Day Out?€?Art and Gardens',
          start: '2024-05-22',
          end: '2024-05-22',
          className: 'bg-gradient-danger',
          category: 'wildlife',
          url: 'https://www.eventbrite.com.au/e/a-day-outart-and-gardens-tickets-847998756107?aff=ebdssbdestsearch'    
        },
        {
          title: 'Pareip / Pre Spring Walk on Country, around Jawbone Reserve',
          start: '2024-08-03',
          end: '2024-08-03',
          className: 'bg-gradient-success',
          category: 'conservation',
          url: 'https://www.eventbrite.com.au/e/pareip-pre-spring-walk-on-country-around-jawbone-reserve-tickets-885410405357?aff=ebdssbdestsearch'
        },
        {
          title: 'Regenerative Urban farming',
          start: '2024-05-14',
          end: '2024-05-14',
          className: 'bg-gradient-danger',
          category: 'wildlife',
          url: 'https://www.eventbrite.com.au/e/regenerative-urban-farming-tickets-764302889517?aff=ebdssbdestsearch'  
        },
        {
          title: 'My Day of Days Exhibition - Mulberry Hill',
          start: '2024-05-05',
          end: '2024-05-05',
          className: 'bg-gradient-danger',
          category: 'wildlife',
          url: 'https://www.eventbrite.com.au/e/my-day-of-days-exhibition-mulberry-hill-tickets-773483338487?aff=ebdssbdestsearch'
        },
        {
          title: 'Explore Jacks Magazine',
          start: '2024-06-02',
          end: '2024-06-02',
          className: 'bg-gradient-success',
          category: 'conservation',
          url: 'https://www.eventbrite.com.au/e/explore-jacks-magazine-tickets-24615576853?aff=ebdssbdestsearch'       
        },
        {
          title: 'Koala Food Tree Planting Day - Mount Martha',
          start: '2024-06-16',
          end: '2024-06-16',
          className: 'bg-gradient-danger',
          category: 'wildlife',
          url: 'https://www.eventbrite.com/e/koala-food-tree-planting-day-mount-martha-tickets-883098500387?aff=ebdssbdestsearch'
        },
        {
          title: 'NATIONAL TREE DAY - Koala Food Tree Planting Day - Moorooduc',
          start: '2024-07-28',
          end: '2024-07-28',
          className: 'bg-gradient-success',
          category: 'conservation',
          url: 'https://www.eventbrite.com/e/national-tree-day-koala-food-tree-planting-day-moorooduc-tickets-884702487957?aff=ebdssbdestsearch'
        },
        {
          title: 'City Nature Challenge 2024 bird walk and water bug survey at Jacana Wetland',
          start: '2024-05-05',
          end: '2024-05-05',
          className: 'bg-gradient-danger',
          category: 'wildlife',
          url: 'https://www.eventbrite.com.au/e/city-nature-challenge-2024-bird-walk-and-water-bug-survey-at-jacana-wetland-tickets-827946619627?aff=ebdssbdestsearch'
        },
        {
          title: 'City Nature Challenge 2024  spot-light walk at Woodlands Historic Park',
          start: '2024-05-04',
          end: '2024-05-04',
          className: 'bg-gradient-danger',
          category: 'wildlife',
          url: 'https://www.eventbrite.com.au/e/city-nature-challenge-2024-spot-light-walk-at-woodlands-historic-park-tickets-827945556447?aff=ebdssbdestsearch'
        },
        {
          title: 'Indigenous Art and Printing at Nomad Gallery',
          start: '2024-05-04',
          end: '2024-05-04',
          className: 'bg-gradient-danger',
          category: 'wildlife',
          url: 'https://www.eventbrite.com.au/e/indigenous-art-and-printing-at-nomad-gallery-tickets-861195668427?aff=ebdssbdestsearch'
        },
        {
          title: 'Cloth Covered Solander Style Box',
          start: '2024-06-29',
          end: '2024-06-29',
          className: 'bg-gradient-danger',
          category: 'wildlife',
          url: 'https://www.eventbrite.com.au/e/cloth-covered-solander-style-box-tickets-800352133777?aff=ebdssbdestsearch'
        },
        {
          title: 'Printmaking with Dana Coleman',
          start: '2024-06-01',
          end: '2024-06-01',
          className: 'bg-gradient-danger',
          category: 'wildlife',
          url: 'https://www.eventbrite.com.au/e/printmaking-with-dana-coleman-tickets-863388758017?aff=ebdssbdestsearch'
        },
        {
          title: 'Sculptural Forms from Nature with Katrina Carter',
          start: '2024-05-25',
          end: '2024-05-25',
          className: 'bg-gradient-danger',
          category: 'wildlife',
          url: 'https://www.eventbrite.com.au/e/sculptural-forms-from-nature-with-katrina-carter-tickets-862072089827?aff=ebdssbdestsearch'
        },
      ],
      eventClick: function(info) {
        window.open(info.event.url, "_blank"); // Open in a new tab
        info.jsEvent.preventDefault(); // Prevent the default browser click action
      },
      views: {
        month: {
          titleFormat: {
            month: "long",
            year: "numeric"
          }
        },
        agendaWeek: {
          titleFormat: {
            month: "long",
            year: "numeric",
            day: "numeric"
          }
        },
        agendaDay: {
          titleFormat: {
            month: "short",
            year: "numeric",
            day: "numeric"
          }
        }
      },
    });

    calendar.render();
    var legendHtml = '<div id="legend" style="display: inline-block; vertical-align: middle;">' +
                   '<div class="legend-item" style="display: inline-block; margin-right: 5px;">' +
                   '<span class="legend-color bg-gradient-danger" style="width: 20px; height: 20px; display: inline-block; vertical-align: middle;"></span> Wildlife' +
                   '</div>' +           
                   '<div class="legend-item" style="display: inline-block;">' +
                   '<span class="legend-color bg-gradient-success" style="width: 20px; height: 20px; display: inline-block; vertical-align: middle;"></span> Conservation' +
                   '</div>' +
                   '</div>';
    // Select the placeholder for the legend and insert the HTML
    var legendElement = document.querySelector('.fc-legend-button');
    if (legendElement) {
      legendElement.innerHTML = legendHtml;
    };
    var ctx1 = document.getElementById("chart-line-1").getContext("2d");

    var gradientStroke1 = ctx1.createLinearGradient(0, 230, 0, 50);

    gradientStroke1.addColorStop(1, 'rgba(255,255,255,0.3)');
    gradientStroke1.addColorStop(0.2, 'rgba(72,72,176,0.0)');
    gradientStroke1.addColorStop(0, 'rgba(203,12,159,0)'); //purple colors

    new Chart(ctx1, {
      type: "line",
      data: {
        labels: ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        datasets: [{
          label: "Visitors",
          tension: 0.5,
          borderWidth: 0,
          pointRadius: 0,
          borderColor: "#fff",
          borderWidth: 2,
          backgroundColor: gradientStroke1,
          data: [50, 45, 60, 60, 80, 65, 90, 80, 100],
          maxBarThickness: 6,
          fill: true
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          }
        },
        interaction: {
          intersect: false,
          mode: 'index',
        },
        scales: {
          y: {
            grid: {
              drawBorder: false,
              display: false,
              drawOnChartArea: false,
              drawTicks: false,
            },
            ticks: {
              display: false
            }
          },
          x: {
            grid: {
              drawBorder: false,
              display: false,
              drawOnChartArea: false,
              drawTicks: false,
            },
            ticks: {
              display: false
            }
          },
        },
      },
    });