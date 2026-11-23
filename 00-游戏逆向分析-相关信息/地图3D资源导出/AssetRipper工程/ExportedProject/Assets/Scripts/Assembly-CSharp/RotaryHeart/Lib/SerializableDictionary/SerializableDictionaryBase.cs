using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace RotaryHeart.Lib.SerializableDictionary
{
	[Serializable]
	public class SerializableDictionaryBase<TKey, TValue> : DrawableDictionary, IDictionary<TKey, TValue>, ICollection<KeyValuePair<TKey, TValue>>, IEnumerable<KeyValuePair<TKey, TValue>>, IEnumerable, ISerializationCallbackReceiver
	{
		private Dictionary<TKey, TValue> _dict;

		private static readonly Dictionary<TKey, TValue> _staticEmptyDict;

		[SerializeField]
		private List<TKey> _keyValues;

		[SerializeField]
		private List<TKey> _keys;

		[SerializeField]
		private List<TValue> _values;

		// C# has no syntax for parameterized property 'Item'.
		public TValue get_Item(TKey key)
		{
			return default;
		}

		public void set_Item(TKey key, TValue value)
		{
		}

		public ICollection<TKey> Keys => null;

		public ICollection<TValue> Values => null;

		public int Count => 0;

		bool ICollection<KeyValuePair<TKey, TValue>>.IsReadOnly => false;

		public void CopyFrom(IDictionary<TKey, TValue> src)
		{
		}

		public void CopyFrom(object src)
		{
		}

		public void CopyTo(IDictionary<TKey, TValue> dest)
		{
		}

		public Dictionary<TKey, TValue> Clone()
		{
			return null;
		}

		public bool ContainsValue(TValue value)
		{
			return false;
		}

		public bool ContainsKey(TKey key)
		{
			return false;
		}

		public void Add(TKey key, TValue value)
		{
		}

		public void Clear()
		{
		}

		public bool Remove(TKey key)
		{
			return false;
		}

		public bool TryGetValue(TKey key, out TValue value)
		{
			value = default;
			return false;
		}

		void ICollection<KeyValuePair<TKey, TValue>>.Add(KeyValuePair<TKey, TValue> item)
		{
		}

		bool ICollection<KeyValuePair<TKey, TValue>>.Contains(KeyValuePair<TKey, TValue> item)
		{
			return false;
		}

		void ICollection<KeyValuePair<TKey, TValue>>.CopyTo(KeyValuePair<TKey, TValue>[] array, int arrayIndex)
		{
		}

		bool ICollection<KeyValuePair<TKey, TValue>>.Remove(KeyValuePair<TKey, TValue> item)
		{
			return false;
		}

		public Dictionary<TKey, TValue>.Enumerator GetEnumerator()
		{
			return default;
		}

		IEnumerator IEnumerable.GetEnumerator()
		{
			return null;
		}

		IEnumerator<KeyValuePair<TKey, TValue>> IEnumerable<KeyValuePair<TKey, TValue>>.GetEnumerator()
		{
			return null;
		}

		void ISerializationCallbackReceiver.OnAfterDeserialize()
		{
		}

		void ISerializationCallbackReceiver.OnBeforeSerialize()
		{
		}
	}
}
