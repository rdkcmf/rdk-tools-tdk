/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2016 RDK Management
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
*/
package com.comcast.rdk

import org.junit.*
import grails.test.mixin.*

/**
 * Test class for primitive test controller.
 *
 */
@TestFor(PrimitiveTestController)
@Mock(PrimitiveTest)
class PrimitiveTestControllerTests {

	/**
	 * To populate valid params
	 * @param params
	 * @return
	 */
	def populateValidParams(params) {
		assert params != null
	}


	/**
	 * to test the save method
	 */
	void testSave() {
		controller.save()

		assert model.primitiveTestInstance != null
		assert view == '/primitiveTest/create'

		response.reset()

		populateValidParams(params)
		controller.save()

		assert response.redirectedUrl == '/primitiveTest/show/1'
		assert controller.flash.message != null
		assert PrimitiveTest.count() == 1
	}


	/**
	 * to test the index.
	 */
	void testIndex() {
		controller.index()
		assert "/primitiveTest/list" == response.redirectedUrl
	}


	/**
	 * to test the list method
	 */
	void testList() {

		def modelObj = controller.list()

		assert modelObj.primitiveTestInstanceList.size() == 0
		assert modelObj.primitiveTestInstanceTotal == 0
	}



	/**
	 * to test the show method
	 */
	void testShow() {
		controller.show()

		assert flash.message != null
		assert response.redirectedUrl == '/primitiveTest/list'
		//check the params
		populateValidParams(params)
		def primitiveTestObj = new PrimitiveTest(params)
		//check the save
		assert primitiveTestObj.save() != null

		params.id = primitiveTestObj.id
		//invoking show
		def model = controller.show()

		assert model.primitiveTestInstance == primitiveTestObj
	}


	/**
	 * to test the delete method
	 */
	void testDelete() {
		controller.delete()
		assert flash.message != null
		assert response.redirectedUrl == '/primitiveTest/list'

		response.reset()
		//check the params
		populateValidParams(params)
		def primitiveTestObj = new PrimitiveTest(params)
		//check the save
		assert primitiveTestObj.save() != null
		assert PrimitiveTest.count() == 1

		params.id = primitiveTestObj.id
		//invoking delete
		controller.delete()

		assert PrimitiveTest.count() == 0
		assert PrimitiveTest.get(primitiveTestObj.id) == null
		assert response.redirectedUrl == '/primitiveTest/list'
	}

	/**
	 * to test the create method
	 */
	void testCreate() {
		def modelObj = controller.create()
		//check the create return
		assert modelObj.primitiveTestInstance != null
	}

	/**
	 * to test the update method
	 */
	void testUpdate() {
		controller.update()

		assert flash.message != null
		assert response.redirectedUrl == '/primitiveTest/list'

		response.reset()
		//check the params
		populateValidParams(params)
		def primitiveTestObj = new PrimitiveTest(params)
		//check the save
		assert primitiveTestObj.save() != null

		params.id = primitiveTestObj.id

		controller.update()

		assert view == "/primitiveTest/edit"
		assert model.primitiveTestInstance != null

		primitiveTestObj.clearErrors()
		//check the params
		populateValidParams(params)
		controller.update()

		assert response.redirectedUrl == "/primitiveTest/show/$primitiveTestObj.id"
		assert flash.message != null

		//test outdated version number
		response.reset()
		primitiveTestObj.clearErrors()
		//check the params
		populateValidParams(params)
		params.id = primitiveTestObj.id
		params.version = -1
		controller.update()

		assert view == "/primitiveTest/edit"
		assert model.primitiveTestInstance != null
		assert model.primitiveTestInstance.errors.getFieldError('version')
		assert flash.message != null
	}

	/**
	 * to test the edit method
	 */
	void testEdit() {

		controller.edit()

		assert flash.message != null
		assert response.redirectedUrl == '/primitiveTest/list'
		//check the params
		populateValidParams(params)
		def primitiveTest = new PrimitiveTest(params)
		// to test the save return
		assert primitiveTest.save() != null

		params.id = primitiveTest.id
		def model = controller.edit()

		assert model.primitiveTestInstance == primitiveTest
	}
}
