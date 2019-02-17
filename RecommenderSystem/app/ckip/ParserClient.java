package ckip;

import java.util.List;

/**
 * Connect CKIP Parser Server.
 *
 * @version 1.0 2017年11月12日
 * @author Alex
 *
 */
public abstract class ParserClient {
    public abstract List parse(String parserQuestion);
}
