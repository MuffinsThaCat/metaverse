/**
 * Copyright (c) 2011-2015 mvs developers (see AUTHORS)
 *
 * This file is part of mvs-node.
 *
 * libbitcoin is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License with
 * additional permissions to the one published by the Free Software
 * Foundation, either version 3 of the License, or (at your option)
 * any later version. For more information see LICENSE.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 */
#ifndef LIBBITCOIN_DATABASE_ACCOUNT_ADDRESS_DATABASE_HPP
#define LIBBITCOIN_DATABASE_ACCOUNT_ADDRESS_DATABASE_HPP
#include <memory>
#include <boost/filesystem.hpp>
#include <bitcoin/bitcoin.hpp>
#include <bitcoin/database/define.hpp>
#include <bitcoin/database/memory/memory_map.hpp>
#include <bitcoin/database/result/account_address_result.hpp>
#include <bitcoin/database/primitives/slab_hash_table.hpp>
#include <bitcoin/database/primitives/slab_manager.hpp>
#include <bitcoin/database/databases/base_database.hpp>
//#include <bitcoin/bitcoin/chain/attachment/account_address/account_address_detail.hpp>

using namespace libbitcoin::chain;

namespace libbitcoin {
namespace database {

/// This enables lookups of account_addresss by hash.
/// An alternative and faster method is lookup from a unique index
/// that is assigned upon storage.
/// This is so we can quickly reconstruct blocks given a list of tx indexes
/// belonging to that block. These are stored with the block.
class BCD_API account_address_database: public base_database
{
public:
    /// Construct the database.
    account_address_database(const boost::filesystem::path& map_filename,
        std::shared_ptr<shared_mutex> mutex=nullptr);

    /// Close the database (all threads must first be stopped).
    ~account_address_database();
	
	/// get account_address info by symbol hash
	account_address_result get_account_address_result(const hash_digest& hash) const;
	
    /// Store a account_address in the database. Returns a unique index
    /// which can be used to reference the account_address.
    void store(const hash_digest& hash, const account_address account_address);
};

} // namespace database
} // namespace libbitcoin

#endif
