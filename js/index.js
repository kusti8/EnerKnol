class SearchResults extends React.Component {
    render() {
        var that = this
        return this.props.results.map(function(item, i) {
                if (item._source) {
                    return (
                        <li style={{listStyleType: "none", backgroundColor: "white", color: "black"}} id={i}>
                            <article>
                                <h1 style={{textAlign: "start"}}><a target="_blank" href={that.props.baseUrl + '?id=' + item._id} rel="external">{item._source.title + " " + item._source.year}</a></h1>
                                <p style={{display: "flex"}}><img src={item._source.image}/><div style={{verticalAlign: "top", padding: "8px"}}>{item._source.description}</div></p>
                            </article>
                        </li>
                    )
                } else {
                    return (
                        <li style={{listStyleType: "none", backgroundColor: "white", color: "black"}} id={i}>
                            <article>
                                <h1 style={{textAlign: "start"}}><a target="_blank" href={that.props.baseUrl + '?id=' + item._id} rel="external">{item.title + " " + item.year}</a></h1>
                                <div style={{display: "flex"}}><img src={item.image}/><div style={{verticalAlign: "top", padding: "8px"}}>{item.description}</div></div>
                            </article>
                        </li>
                    )
                }
                })
        }
}

function renderSearchResults(results, baseUrl) {
    ReactDOM.render(<SearchResults results={results} baseUrl={baseUrl}/>, document.getElementById('search-results'))
}