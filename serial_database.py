from typing import Callable, Dict, List

from database import CachingDatabaseWrapper, Database, Optional, Transaction

class SerialTransactionExecutor:
    def __init__(self, db: 'SerialDatabase', txn: Transaction) -> None:
        self.db = db
        self.cached_db = CachingDatabaseWrapper(db)
        self.txn = txn
        self.start_tn = self.db._get_tnc()

    def read_phase(self) -> None:
        self.txn(self.cached_db)
        print("Read phase")

    def validate_and_write_phase(self) -> bool:
        finish_tn = self.db._get_tnc()
        print("Langkah ke :",finish_tn)
        for tn in range(self.start_tn + 1, finish_tn + 1):
            cached_db = self.db._get_transaction(tn)
            write_set = cached_db.get_write_set()
            read_set = self.cached_db.get_read_set()
            if not write_set.isdisjoint(read_set):
                print("Abort")
                return False
        self.db._commit_transaction(self.cached_db)
        print("write")
        return True

class SerialDatabase(Database):
    def __init__(self) -> None:
        Database.__init__(self)
        self.transactions: Dict[int, CachingDatabaseWrapper] = {}
        self.tnc: int = 0

    def _get_tnc(self) -> int:
        return self.tnc

    def _get_transaction(self, tn: int) -> CachingDatabaseWrapper:
        assert tn in self.transactions
        return self.transactions[tn]

    def _commit_transaction(self, db: CachingDatabaseWrapper) -> None:
        self.tnc += 1
        assert self.tnc not in self.transactions
        self.transactions[self.tnc] = db
        db.commit()
        print("commit")

    # Ngasih tau variabel mana aja yang mau diincrement
    def begin(self, txn: Transaction) -> SerialTransactionExecutor:
        return SerialTransactionExecutor(self, txn)

def main():
    def init(db: CachingDatabaseWrapper) -> None:
        db.write('x', 0)
        db.write('y', 0)
        db.write('z', 0)

    def incr_vars(vs: List[str]) -> Transaction:
        def txn(db: CachingDatabaseWrapper) -> None:
            for v in vs:
                x = db.read(v)
                db.write(v, x + 1)
                print(v)
                print(x)
        return txn
    def get_digit(str1):
        c = ""
        for i in str1:
            if i.isdigit():
                c += i
        return int(c)
    def beginTransaction(str):
        tranNumber = get_digit(str)
        print("============================ Begin Transaction %d =============================" % (tranNumber))
        #temp = int(len(transactionTableObjects)) + 1
        #transactionTableObjects.append(transactionTable(tranNumber, temp, AC))

    #==============================================================BUAT INPUT==============================================================
    incr_x = incr_vars(['x'])
    incr_y = incr_vars(['y'])
    incr_z = incr_vars(['z'])
    incr_all = incr_vars(['x', 'y', 'z'])

    transaksi = [[], [], []]

    db = SerialDatabase()
    assert(db.data == {})
    #print("db.data = " + str(db.data))

    statusTrans = []
    inputDariFile = []
    n = 0
    with open("input.txt", 'r') as text:
        for line in text:
            inputDariFile.append(line)
    for operasi in inputDariFile:
        #print(operasi)
        if operasi.find('b') == 1:
            pass
            #print("=====================================MULAI=====================================")

        if operasi.find('b') != -1:
            statusTrans.append(True)
            n += 1
            #beginTransaction(operasi)
            tranNumber = get_digit(operasi)
            if(tranNumber != n):
                statusTrans[n-1] = False
        elif operasi.find('r') != -1:
            #print("=====================================READ=====================================")
            tranNumber = get_digit(operasi)
            transaksi[n-1].append(tranNumber)
            n = tranNumber
        elif operasi.find('w') != -1:
            #print("=====================================WRITE=====================================")
            tranNumber = get_digit(operasi)
            temp = True
            for isi in transaksi[tranNumber-1]:
                if(isi != n):
                    temp = False
                print("Isinya adalah: " + str(isi))
            statusTrans[n-1] = temp
        elif operasi.find("e") != -1:
            pass
            #print("=====================================END=====================================")
        #print(operasi)
    for i in range(0, len(statusTrans)):
        if (statusTrans[i] == False):
            print("Validasi T"+str(i+1)+" gagal dieksekusi")
        else:
            print("Validasi T"+str(i+1)+" berhasil dieksekusi")
    print(transaksi)
    print(statusTrans)


    """
    incr_x = incr_vars(['x'])
    incr_y = incr_vars(['y'])
    incr_z = incr_vars(['z'])
    incr_all = incr_vars(['x', 'y', 'z'])

    db = SerialDatabase()
    assert(db.data == {})
    print(db.data)

    t_init = db.begin(init)
    t_init.read_phase()
    assert(t_init.validate_and_write_phase())
    #assert(db.data == {'x': 0, 'y': 0, 'z': 0})
    print(db.data)

    # t_1 and t_2 run concurrently and have conflicting read and write sets, so
    # whichever transaction attempts to commit first (i.e. t_1) succeeds. The
    # other (i.e. t_2) fails and is forced to abort.
    print("T1 DAN T2")
    t_1 = db.begin(incr_all)
    t_2 = db.begin(incr_all)
    t_1.read_phase()
    t_2.read_phase()
    assert(t_1.validate_and_write_phase())
    assert(not t_2.validate_and_write_phase())
    assert(db.data == {'x': 1, 'y': 1, 'z': 1})
    print(db.data)

    # t_3 and t_4 run concurrently, but have disjoint read and write sets, so
    # they can both commit.
    print("T3 DAN T4")
    t_3 = db.begin(incr_x)
    t_4 = db.begin(incr_y)
    t_3.read_phase()
    t_4.read_phase()
    assert(t_3.validate_and_write_phase())
    assert(t_4.validate_and_write_phase())
    assert(db.data == {'x': 2, 'y': 2, 'z': 1})
    print(db.data)
    """

if __name__ == '__main__':
    main()
