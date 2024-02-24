function vereineProSpiel(teams){
    teams = JSON.parse(teams);
    const spiel = document.getElementById('spiel');
    const selected = spiel.options[spiel.selectedIndex];
    const heim = selected.getAttribute("heim");
    const gast = selected.getAttribute("gast");
    const options = document.getElementById('team').options;
    while(options.length > 1){
        options.remove(1);
    }
    for(let team of teams){
        if(team[0] == heim || team[0] == gast){
            const option = new Option(team[1]+", "+team[2], team[0])
            options.add(option);
        }
    }
}
