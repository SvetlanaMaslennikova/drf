import React from "react"
import {Link} from "react-router-dom"


const AuthorItem = ({author}) => {
    return (
        <tr>
            <td>
                <Link to={`author/${author.id}`}>{author.id}</Link>
            </td>
            <td>
                {author.first_name}
            </td>
            <td>
                {author.birthday_year}
            </td>
        </tr>
    )
}


const AuthorList = ({authors}) => {
    return (
        <table>
            <th>
                ID
            </th>
            <th>
                First name
            </th>
            <th>
                Birthday year
            </th>
            {authors.map((author) => <AuthorItem author={author} />)}
        </table>
    )
}


export default AuthorList
