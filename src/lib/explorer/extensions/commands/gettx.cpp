/**
 * Copyright (c) 2016-2017 mvs developers 
 *
 * This file is part of metaverse-explorer.
 *
 * metaverse-explorer is free software: you can redistribute it and/or
 * modify it under the terms of the GNU Affero General Public License with
 * additional permissions to the one published by the Free Software
 * Foundation, either version 3 of the License, or (at your option)
 * any later version. For more information see LICENSE.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 */

#include <metaverse/explorer/json_helper.hpp>
#include <metaverse/explorer/dispatch.hpp>
#include <metaverse/explorer/extensions/commands/gettx.hpp>
#include <metaverse/explorer/extensions/command_extension_func.hpp>
#include <metaverse/explorer/extensions/command_assistant.hpp>
#include <metaverse/explorer/extensions/exception.hpp>

namespace libbitcoin {
namespace explorer {
namespace commands {


/************************ gettx *************************/
/// extent fetch-tx command , add tx height in tx content
console_result gettx::invoke (std::ostream& output,
        std::ostream& cerr, libbitcoin::server::server_node& node)
{
    bc::chain::transaction tx;
    uint64_t tx_height = 0;
    auto& blockchain = node.chain_impl();
    auto exist = blockchain.get_transaction(argument_.hash, tx, tx_height);
    if(!exist)
        throw tx_notfound_exception{"transaction does not exist!"};
    
    if (option_.json) {
        output << config::json_helper().prop_list(tx, tx_height, true).toStyledString();
    } else {
        config::transaction config_tx{tx};
        output << config::json_helper().prop_tree(config_tx, false).toStyledString();
    }

    return console_result::okay;
}


} // namespace commands
} // namespace explorer
} // namespace libbitcoin

