<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <html>
            <head>
                <meta charset="utf-8"/>
            </head>
            <body>
                <h2 align="center">Products</h2>
                <table border="1" width="80%" align="center">
                    <tr bgcolor="#dfdfdf" width="80%">
                        <th>Image</th>
                        <th>Description</th>
                        <th>Price</th>
                    </tr>
                    <xsl:for-each select="data/item">
                        <tr>
                            <td>
                                <img style="padding: 16">
                                    <xsl:attribute name="src">
                                        <xsl:value-of select="image"/>
                                    </xsl:attribute>
                                </img>
                            </td>
                            <td>
                                <xsl:value-of select="description"/>
                            </td>
                            <td>
                                <xsl:value-of select="price"/>
                            </td>
                        </tr>
                    </xsl:for-each>
                </table>
            </body>
        </html>
    </xsl:template>

</xsl:stylesheet>