package Cognifyz.Task_5_CRUD_Operation_with_Persistent_Data.repository;
import Cognifyz.Task_5_CRUD_Operation_with_Persistent_Data.entity.JournalEntry;
import org.bson.types.ObjectId;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface JournalEntryRepository extends MongoRepository<JournalEntry, ObjectId> {
}
